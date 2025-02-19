install-precommit:
	pre-commit install

run-precommit:
	pre-commit run --all-files

test:
	pytest -vv
