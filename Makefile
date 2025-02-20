install-precommit:
	pre-commit install

run-precommit:
	pre-commit run --all-files

test:
	export PYTHONPATH="${PYTHONPATH}:$(pwd)" && \
	pytest -vv
