PROJECT=expressive_regex

.PHONY: install
install:
	curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
	# for windows comment the line above and uncomment the next line, for powershell only the next line
	# powershell "(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python"
	poetry install

.PHONY: install-packages
install-packages:
	poetry install

.PHONY: install-packages
update:
	poetry update

.PHONY: lock
lock:
	poetry lock

.PHONY: build
build:
	poetry build

.PHONY: clean
clean:
	git clean -fxd

.PHONY: lint
lint:
	poetry run pylint ${PROJECT} -f colorized -d missing-module-docstring,missing-class-docstring,missing-function-docstring,invalid-name || poetry run pylint-exit $$?

.PHONY: test-full
test-full:
	poetry run pytest ${PROJECT} tests --doctest-modules --cov=${PROJECT} --cov-report=xml --cov-config=.coveragerc -v

.PHONY: coverage
coverage:
	poetry run pytest ${PROJECT} tests --doctest-modules --cov=${PROJECT} --cov-config=.coveragerc --cov-report=html -v

.PHONY: cov
cov:
	poetry run codecov

.PHONY: publish
publish:
	poetry config http-basic.pypi ${PYPI_USER} ${PYPI_PASSWORD}
	poetry publish

.PHONY: publish-token
publish-token:
	poetry config pypi-token.pypi ${POETRY_PYPI_TOKEN_PYPI}
	poetry publish

# Below are the commands that will be run INSIDE the development environment, i.e., inside Docker or Travis
# These commands are NOT supposed to be run by the developer directly, and will fail to do so.

.PHONY: dev-install
dev-install:
	pip install poetry
	poetry config virtualenvs.create false
	poetry install

.PHONY: dev-test
dev-test:
	python -m pylint ${PROJECT} -f colorized -d missing-module-docstring,missing-class-docstring,missing-function-docstring,invalid-name || python -m pylint_exit $$?
	python -m pytest ${PROJECT} tests --doctest-modules --cov=${PROJECT} --cov-report=xml --cov-config=.coveragerc -v

.PHONY: dev-cov
dev-cov:
	python -m codecov
