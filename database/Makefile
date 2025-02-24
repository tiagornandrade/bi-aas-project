up:
	docker-compose up -d

down:
	docker-compose down

restart:
	docker-compose restart

run-migrations:
	python src/utils/migrations.py

run-main:
	python src/main.py

# export $(xargs <.env)
# export PYTHONPATH="${PYTHONPATH}:$(pwd)"

install:
	pip install -r requirements.txt

test:
	export PYTHONPATH="${PYTHONPATH}:$(pwd)" && \
	pytest -vv  --junitxml=test-results-database.xml

ci: install test
