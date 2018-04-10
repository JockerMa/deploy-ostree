ifeq ($(OS),Windows_NT)
	PYTHON := py -3
else
	PYTHON := python3
endif

dummy:
	@echo please select a target explicitly

lint:
	flake8 .
	mypy . \
		--ignore-missing-imports \
		--check-untyped-defs

_test:
	$(PYTHON) setup.py test

qc: lint _test
