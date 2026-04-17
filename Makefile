init:
#	Это выкидывает ошибку на маке
    python -m pip install poetry==1.8.2

#	проще так:
# 	brew install poetry

	poetry install --no-root

ci-test:
	poetry run pytest -sv homework/tests

test:
	act -j build --container-architecture linux/amd64

format:
	poetry run ruff format .

lint:
	poetry run ruff check .
