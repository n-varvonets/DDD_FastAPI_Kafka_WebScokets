# DDD: Entities, Domain, и Use Cases

## Являются ли Entities (Сущности) частью Domain (Домена)?

Да, **Entities** являются частью **Domain**. Однако важно понимать, что **домен** — это не только сущности, но и вся бизнес-логика, правила и инварианты, управляющие предметной областью.

### Что такое Entity в DDD?
**Entity** (сущность) — это объект с уникальным идентификатором (ID), который сохраняет свою идентичность на протяжении всего жизненного цикла.
Примеры сущностей:
- `User(id, name, email)`
- `Order(id, items, totalPrice)`
- `Product(id, name, price)`

Сущности содержат данные и могут включать базовую бизнес-логику, но они **не определяют всю предметную область**.

[а что определяет предметную область?](subject%20area.md)

## Может ли Entity быть несвязана с Domain?

Сама по себе **Entity** без контекста не представляет ценности. Если рассматривать её отдельно от домена, она может выступать просто как объект данных (например, DTO или ORM-модель). Однако в DDD **Entity является частью домена** и используется для моделирования предметной области.

### В чем разница между Domain и Infrastructure?
- **Domain (Домен)** содержит бизнес-логику, включая **сущности, агрегаты, value objects и доменные события**.
- **Infrastructure (Инфраструктура)** занимается техническими аспектами, такими как работа с базой данных, API, логирование.

## Как Domain является центральной сущностью, но ничего не знает о внешнем мире?

DDD предполагает **разделение ответственности**:
- **Домен** должен быть чистым и **не зависеть** от инфраструктуры, API или БД.
- **Use Cases** (Application Layer) управляют процессами, вызывая нужные методы домена.

Это позволяет **домену быть независимым**, легко тестируемым и переносимым в разные проекты или технологии.

## Что такое Use Case в DDD?

**Use Case** (сценарий использования) определяет **конкретный бизнес-процесс**, оркестрируя взаимодействие между доменными объектами и внешними системами.

Пример Use Case:
```python
class PlaceOrderUseCase:
    def __init__(self, order_repository, payment_service):
        self.order_repository = order_repository
        self.payment_service = payment_service
    
    def execute(self, user_id, items):
        order = Order.create(user_id, items)
        self.order_repository.save(order)
        self.payment_service.process_payment(order)
        return order
```

### Чем Use Case отличается от сервиса?
- **Use Case** отвечает за **выполнение бизнес-операции**.
- **Service** — это вспомогательный слой, который **инкапсулирует логику, но не управляет процессом**.

### Где накапливать события (Events)?
DDD предлагает хранить **Domain Events** в **Use Case** или в **самих доменных объектах**. 
Пример событий в домене:
```python
class Order:
    def place_order(self):
        self.status = 'PLACED'
        self.events.append(OrderPlacedEvent(self.id))
```

## Пример полного пути ивента через архитектуру

### 1. Ивент создается в домене и передается через репозиторий и сервис в Use Case:

```python
# domain/events.py
class OrderPlacedEvent:
    def __init__(self, order_id):
        self.order_id = order_id
```

```python
# domain/models.py
class Order:
    def __init__(self, id, items):
        self.id = id
        self.items = items
        self.events = []

    def place_order(self):
        self.events.append(OrderPlacedEvent(self.id))
```

```python
# infrastructure/repository.py
class OrderRepository:
    def save(self, order):
        # Логика сохранения заказа в БД
        return order
```

```python
# application/services.py
class OrderService:
    def __init__(self, order_repository):
        self.order_repository = order_repository
    
    def process_order(self, order):
        self.order_repository.save(order)
        return order.events
```

```python
# application/use_cases.py
class PlaceOrderUseCase:
    def __init__(self, order_service):
        self.order_service = order_service
    
    def execute(self, order):
        events = self.order_service.process_order(order)
        for event in events:
            print(f"Event {event.__class__.__name__} triggered for order {event.order_id}")
```

### 2. Ивент создается в Use Case и передается в домен
```python
# application/use_cases.py
class CancelOrderUseCase:
    def __init__(self, order_repository):
        self.order_repository = order_repository
    
    def execute(self, order_id):
        order = self.order_repository.get_by_id(order_id)
        order.cancel()
        self.order_repository.save(order)
```

```python
# domain/models.py
class Order:
    def cancel(self):
        self.status = 'CANCELLED'
        self.events.append(OrderCancelledEvent(self.id))
```

## Заключение
- **Entities (Сущности)** — это часть домена, но сам домен шире.
- **Домен** не должен знать о технологиях, API или БД.
- **Use Cases** управляют процессами и координируют работу доменных объектов.
- **События** можно хранить в Use Case или в самих доменных моделях.
- **Ивенты могут идти от домена к Use Case и обратно**.

Это разделение повышает **гибкость, тестируемость и масштабируемость** архитектуры.
