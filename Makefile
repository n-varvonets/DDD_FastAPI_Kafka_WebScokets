DC = docker compose
EXEC = docker exec -it
LOGS = docker logs
ENV = --env-file .env
APP_FILE = docker_compose/app.yaml
STORAGES_FILE = docker_compose/storages.yaml
APP_CONTAINER = main-app

.PHONY: app
app:
	$(DC) -f $(APP_FILE) $(ENV) up --build -d


.PHONY: all
all:
	$(DC) -f $(APP_FILE) -f $(STORAGES_FILE) $(ENV) up --build -d


.PHONY: app-storages
app-storages:
	$(DC) -f $(STORAGES_FILE) $(ENV) up --build -d


.PHONY: app-down
app-down:
	$(DC) -f $(APP_FILE) down


.PHONY: app-storages-down
app-storages-down:
	$(DC) -f $(STORAGES_FILE) down


.PHONY: all-down
all-down:
	$(DC) -f $(APP_FILE) -f $(STORAGES_FILE) down

.PHONY: app-shell
app-shell:
	$(EXEC) $(APP_CONTAINER) /bin/bash

.PHONY: app-logs
app-logs:
	$(LOGS) $(APP_CONTAINER) -f

.PHONY: test
test:
	$(EXEC) $(APP_CONTAINER) pytest
