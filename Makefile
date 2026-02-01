SHELL := /bin/bash

STACK ?= postgres
ENV_FILE := infra/env/.env

BASE := -f infra/compose/base.yml

STACK_postgres := -f infra/compose/postgres.yml
STACK_jupyter := -f infra/compose/jupyter.yml

# composites
STACK_postgres_jupyter := $(STACK_postgres) $(STACK_jupyter)

FILES = $(BASE) $(STACK_$(STACK))

.PHONY: up down ps logs smoke reset

up:
	@[ -f $(ENV_FILE) ] || (echo "Missing $(ENV_FILE). Create it: cp infra/env/.env.example infra/env/.env" && exit 1)
	docker compose --env-file $(ENV_FILE) $(FILES) up -d --remove-orphans

down:
	@[ -f $(ENV_FILE) ] || (echo "Missing $(ENV_FILE). Create it: cp infra/env/.env.example infra/env/.env" && exit 1)
	docker compose --env-file $(ENV_FILE) $(FILES) down --remove-orphans

ps:
	@[ -f $(ENV_FILE) ] || (echo "Missing $(ENV_FILE). Create it: cp infra/env/.env.example infra/env/.env" && exit 1)
	docker compose --env-file $(ENV_FILE) $(FILES) ps

logs:
	@[ -f $(ENV_FILE) ] || (echo "Missing $(ENV_FILE). Create it: cp infra/env/.env.example infra/env/.env" && exit 1)
	docker compose --env-file $(ENV_FILE) $(FILES) logs -f --tail=200

smoke:
	bash infra/scripts/smoke.sh $(STACK)

reset:
	bash infra/scripts/reset.sh $(STACK)
