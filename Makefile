include .env
export $(shell sed 's/=.*//' .env)

export PYTHONPATH=$(CURDIR)

define set_user_id
    export USER_ID=$(shell id -u)
	$(eval export USER_ID=$(shell id -u))
endef

.PHONY: help
help: ## Command help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: build-pg
build-pg: ## Build PostgreSQL with PGRouting library
	@docker-compose build

.PHONY: infra-start
infra-start: ## Start infra
	@docker-compose up

.PHONY: setup
setup: ## Setup libraries
	@poetry install

.PHONY: create-index
create-index: ## Create index
	@poetry run python create-index.py

.PHONY: import-correios-files
import-correios-files: ## Import Correios Data Files
	@poetry run python correios-importer.py

.PHONY: import-opensearch
import-opensearch: ## Import Correios Data
	@poetry run python opensearch-importer.py

.PHONY: search-address
search-address: ## Start Search Address App
	@poetry run python search-document.py

.PHONY: delete-index
delete-index: ## Delete index
	@poetry run python delete-index.py

.PHONY: infra-stop
infra-stop: ## Stop infra
	@docker-compose down
