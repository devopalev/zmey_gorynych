PROJECT_NAME=zmey_gorynych

setup-depends:
	poetry install --with=main,dev,test
	poetry run pre-commit install
	cp .env.example .env

setup-dev-db:
	docker run --name $(PROJECT_NAME)-dev-postgres --env-file .env -d -p 6434:5432 postgres

setup: setup-depends setup-dev-db

checks:
	git add .
	pre-commit run

checks-all:
	pre-commit run --all-files

run-tests:
	pytest

up:
	docker-compose up -d

runserver:
	python app.py