
# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SOURCEDIR     = docs
BUILDDIR      = "$(SOURCEDIR)/_build"

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

cov-report = true
lint:
	pipenv run flake8 security_interface
	pipenv run black -l 100 --check tests security_interface

format:
	pipenv run black -l 100 tests/ security_interface/ demo/

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
