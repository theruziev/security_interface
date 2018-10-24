cov-report = true

lint:
	pipenv run flake8 security_interface
	pipenv run black -l 100 --check tests security_interface

format:
	pipenv run black -l 100 tests/ security_interface/

install-dev:
	pipenv install --skip-lock -d

test:
	pipenv run coverage run -m pytest tests
	@if [ $(cov-report) = true ]; then\
    pipenv run coverage combine;\
    pipenv run coverage report;\
	fi

_release:
	scripts/make_release

release: test _release

freeze:
	pipenv lock -d
