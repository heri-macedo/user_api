SHELL := /bin/bash
export FLASK_APP=api:create_app
export PYTHONPATH := $(shell pwd)

.PHONY: run-tests-local run-flask install-requirements run-dev build-env

run-tests:
	docker compose build --no-cache test
	docker compose run --rm test

run-dev:
	docker compose build --no-cache dev
	docker compose up dev

install-requirements:
	pip install -r requirements.txt

run-flask:
	flask run --host=0.0.0.0 --port=5000 

run-tests-local:
	pytest -v --disable-warnings