
# Общий подход в DDD: Медиатор и контейнер для управления зависимостями

## Понятие Медиатора в DDD

- В DDD медиатор может быть использован для уменьшения прямой связи между различными частями приложения, например, между UI, бизнес-логикой и доступом к данным. Он действует как центральный орган, который занимается передачей сообщений или команд от одной части системы к другой, тем самым уменьшая количество прямых связей между компонентами и поддерживая принципы чистой архитектуры.

## Медиаторы и контейнеры для управления зависимостями

### Цель

- **Медиаторы** используются для уменьшения прямой связности между компонентами программы, облегчая их независимую модификацию и тестирование. Медиаторы обрабатывают взаимодействие между компонентами, передавая сообщения или команды от одного компонента к другому.


- **Контейнеры для управления зависимостями** (например, `punq` в Python) помогают автоматизировать процесс инъекции зависимостей. Это позволяет разработчикам легче управлять жизненным циклом объектов и зависимостями между различными частями приложения.
  - **`register()`**: Метод используется для регистрации типов и их реализаций в контейнере. Он позволяет указать, какой объект или класс должен использоваться, когда запрашивается определенный интерфейс или базовый класс.
  - **`resolve()`**: Метод, который возвращает экземпляр объекта на основе его типа. Реализация зависит от регистрации в `register()`, обеспечивая гибкость и удобство управления зависимостями.
  
### Пример использования с аналогией

Представьте, что у вас есть шкафчик с ящиками, в каждом из которых лежат разные игрушки. Каждый ящик маркирован: в одном лежат машинки, в другом — куклы, в третьем — конструкторы. Когда вы хотите поиграть с машинками, вы открываете ящик, где они находятся, и берете машинку.

В программировании `resolve()` работает похожим образом. Этот метод позволяет запросить конкретный тип объекта, и контейнер найдет и создаст нужный экземпляр, как "доставая игрушку из ящика".

### Кодовый пример

```python
from punq import Container

class UserRepository:
    """Интерфейс для работы с данными пользователей."""
    def get_user(self, user_id):
        pass

class MemoryUserRepository(UserRepository):
    """Реализация хранения данных пользователей в памяти."""
    def get_user(self, user_id):
        print(f"Получение пользователя с ID {user_id} из памяти")

class DatabaseUserRepository(UserRepository):
    """Реализация хранения данных пользователей в базе данных."""
    def get_user(self, user_id):
        print(f"Получение пользователя с ID {user_id} из базы данных")

# Работа с контейнером
container = Container()
container.register(UserRepository, MemoryUserRepository)

user_repo = container.resolve(UserRepository)
user_repo.get_user(123)
# Вывод: Получение пользователя с ID 123 из памяти
```

## Как всё это связывается

1. **Entrypoints (views.py)** получают запросы от клиента и вызывают сервисы.
2. **Services** выполняют бизнес-логику, используя сущности и репозитории.
3. **Repositories** управляют доступом к данным через ORM, абстрагируя инфраструктурные детали.
4. **Utils** предоставляют общие функции, используемые как в сервисах, так и в точках входа.
5. **Mediator** координирует взаимодействие между командами и их обработчиками, обеспечивая центральную маршрутизацию команд внутри системы.

### Роль медиатора в этом процессе

Медиатор используется для обработки и маршрутизации команд, что позволяет разделить ответственность за выполнение команд и событий между различными частями системы. Медиатор принимает команду от `Entrypoint` (например, из представления `views.py`), определяет, какой обработчик должен выполнить эту команду, и направляет её нужному обработчику.

### Пример использования медиатора

Предположим, что у нас есть команда для создания нового чата — `CreateChatCommand`. Медиатор получает эту команду из контроллера и перенаправляет её на обработчик `CreateChatCommandHandler`, который отвечает за выполнение логики создания чата.

```python
# application/views.py (Entrypoint)
from rest_framework.views import APIView
from rest_framework.response import Response
from logic.mediator import Mediator
from logic.commands.messages import CreateChatCommand

class CreateChatView(APIView):
    def post(self, request):
        # Получаем данные из запроса
        chat_data = request.data
        
        # Создаем команду для медиатора
        command = CreateChatCommand(chat_data=chat_data)
        
        # Отправляем команду медиатору
        mediator = Mediator()
        result = mediator.send(command)
        
        # Возвращаем ответ клиенту
        return Response({"status": "Chat created", "chat_id": result.chat_id})
```

### Как медиатор обрабатывает команду

В этом примере медиатор получает команду `CreateChatCommand` из `CreateChatView`. Медиатор знает, что для этой команды существует соответствующий обработчик `CreateChatCommandHandler`, и направляет команду ему.

```python
# logic/mediator.py
class Mediator:
    def __init__(self):
        self.handlers = {}

    def register_command(self, command_type, handler):
        # Регистрация команды и её обработчика
        self.handlers[command_type] = handler

    def send(self, command):
        # Находит обработчик для команды и вызывает его
        command_type = type(command)
        handler = self.handlers.get(command_type)
        
        if handler:
            return handler.handle(command)
        else:
            raise Exception(f"No handler found for command {command_type}")
```

### Обработчик команды

Обработчик `CreateChatCommandHandler` принимает команду от медиатора и выполняет необходимую бизнес-логику для создания чата. Например, он может сохранить данные в базе данных через репозиторий.

```python
# logic/commands/messages.py
class CreateChatCommand:
    def __init__(self, chat_data):
        self.chat_data = chat_data

class CreateChatCommandHandler:
    def __init__(self, chat_repository):
        self.chat_repository = chat_repository

    def handle(self, command: CreateChatCommand):
        # Логика создания чата
        chat = self.chat_repository.create_chat(command.chat_data)
        return chat
```

### Взаимодействие с репозиторием

Обработчик `CreateChatCommandHandler` использует репозиторий для сохранения данных чата в базе данных. Репозиторий абстрагирует детали работы с базой данных, предоставляя удобный интерфейс для создания и управления записями.

```python
# infra/repositories/messages.py
class MemoryChatRepository:
    def create_chat(self, chat_data):
        # Здесь могла бы быть логика для сохранения чата в базе данных
        print(f"Сохранение чата: {chat_data}")
        return {"chat_id": 1}  # Возвращаем ID созданного чата как пример
```

### Подведение итогов

1. **Entrypoints** (`CreateChatView`) получают запрос от клиента и создают команду `CreateChatCommand`.
2. **Mediator** принимает команду и направляет её в соответствующий обработчик (`CreateChatCommandHandler`), который зарегистрирован для этой команды.
3. **Command Handler** выполняет бизнес-логику команды и взаимодействует с **Repository** для сохранения данных.
4. **Repository** управляет взаимодействием с базой данных, создавая запись для чата.

Таким образом, медиатор действует как диспетчер, который направляет команды к соответствующим обработчикам, что помогает уменьшить связанность между слоями и сделать код более гибким и легко тестируемым.