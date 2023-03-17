.ONESHELL:

py := poetry run
python := $(py) python

package_dir := src
tests_dir := tests

code_dir := $(package_dir) $(tests_dir)


define setup_env
    $(eval ENV_FILE := $(1))
    @echo " - setup env $(ENV_FILE)"
    $(eval include $(1))
    $(eval export)
endef

.PHONY: reformat
reformat:
	poetry run black --line-length=79 src
	poetry run isort src

.PHONY: dev-web
dev-web:
	$(call setup_env, .env.dev)
	$(python) -m src.presentation.api


.PHONY: dev-docker
dev-docker:
	docker compose -f=docker-compose-dev.yml --env-file=.env.dev up

.PHONY: tests
tests:
	$(call setup_env, .env.test)
	$(py) pytest $(tests_dir) --tb=long 

.PHONY: dev-env
dev-env:
	$(call setup_env, .env.dev)
	$(filter-out $@,$(MAKECMDGOALS))
