SHELL := /bin/bash

STACK ?= postgres
ENV_FILE := infra/env/.env

BASE := -f infra/compose/base.yml

STACK_postgres := -f infra/compose/postgres.yml
STACK_jupyter := -f infra/compose/jupyter.yml
STACK_bigdata-core := -f infra/compose/bigdata-core.yml
STACK_airflow_postgres := -f infra/compose/airflow-postgres.yml
STACK_hive := -f infra/compose/hive.yml
STACK_postgres_tgt := -f infra/compose/postgres-tgt.yml

# composites
STACK_postgres_jupyter := $(STACK_postgres) $(STACK_jupyter)
STACK_airflow_bigdata := $(STACK_airflow_postgres) $(STACK_bigdata-core) $(STACK_hive) $(STACK_postgres_tgt)

STACK_FILES := $(strip $(STACK_$(STACK)))
FILES := $(BASE) $(STACK_FILES)

.PHONY: up down ps logs smoke reset bootstrap check-env check-stack

check-env:
	@[ -f $(ENV_FILE) ] || (echo "Missing $(ENV_FILE). Create it: cp infra/env/.env.example infra/env/.env" && exit 1)

check-stack:
	@[ -n "$(STACK_FILES)" ] || (echo "Unknown STACK=$(STACK)" && exit 1)

up: check-env check-stack
	docker compose --env-file $(ENV_FILE) $(FILES) up -d --remove-orphans

down: check-env check-stack
	docker compose --env-file $(ENV_FILE) $(FILES) down --remove-orphans

ps: check-env check-stack
	docker compose --env-file $(ENV_FILE) $(FILES) ps

logs: check-env check-stack
	docker compose --env-file $(ENV_FILE) $(FILES) logs -f --tail=200

smoke: check-env check-stack
	bash infra/scripts/smoke.sh $(STACK)

reset: check-env check-stack
	bash infra/scripts/reset.sh $(STACK)

bootstrap: check-env check-stack
	bash infra/scripts/bootstrap.sh $(STACK)
