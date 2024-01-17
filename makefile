run_all:
	docker-compose -f docker-compose.yml up --build

run_no_cache:
	docker-compose -f docker-compose.yml build --no-cache
	docker-compose -f docker-compose.yml up

alembic_migrate:
	alembic upgrade head