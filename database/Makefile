up:
	docker-compose up -d

down:
	docker-compose down

restart:
	docker-compose restart

run-migrations:
	python src/utils/migrations.py

run-main:
	export PYTHONPATH="${PYTHONPATH}:$(pwd)" && \
	python src/main.py

# export $(xargs <.env)
