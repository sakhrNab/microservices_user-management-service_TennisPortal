ifneq (,$(wildcard ./.env))
include .env
export
ENV_FILE_PARAM = --env-file .env

endif

build:
	docker compose up --build -d --remove-orphans

up:
	docker compose up -d

down:
	docker compose down

show-logs:
	docker compose logs

migrate:
	docker compose exec user_manage_api3 python manage.py migrate

makemigrations:
	docker compose exec user_manage_api3 python manage.py makemigrations

superuser:
	docker compose exec user_manage_api3 python manage.py createsuperuser

collectstatic:
	docker compose exec user_manage_api3 python manage.py collectstatic --no-input --clear

down-v:
	docker compose down -v

volume:
	docker volume inspect user_management_postgres_data

restart-nginx:
	docker compose exec nginx3 nginx -s reload

user-db:
	docker compose exec postgres-db3 psql --username=admin --dbname=tennis_db

test:
	docker compose exec user_manage_api3 pytest -p no:warnings --cov=.

test-html:
	docker compose exec user_manage_api3 pytest -p no:warnings --cov=. --cov-report html

flake8:
	docker compose exec user_manage_api3 flake8 .

black-check:
	docker compose exec user_manage_api3 black --check --exclude=migrations .

black-diff:
	docker compose exec user_manage_api3 black --diff --exclude=migrations .

black:
	docker compose exec user_manage_api3 black --exclude=migrations .

isort-check:
	docker compose exec user_manage_api3 isort ./ --check-only --skip env --skip migrations

isort-diff:
	docker compose exec user_manage_api3 isort . --diff --skip env --skip migrations

isort:
	docker compose exec user_manage_api3 isort . --skip env --skip migrations