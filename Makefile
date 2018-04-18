ifeq ($(OS),Windows_NT)
	PYTHON := py -3
else
	PYTHON := python3
endif

dummy:
	@echo please select a target explicitly

# plain linting/test targets
lint:
	flake8 .
	mypy . \
		--ignore-missing-imports \
		--check-untyped-defs

all-tests:
	$(PYTHON) -m unittest discover -v -t . -s tests

qc/host: lint all-tests

unit:
	$(PYTHON) -m unittest discover -v -t . -s tests/unit

# Debian
image/debian:
	docker build -t deploy-ostree-debian -f Dockerfile.debian .

qc/debian: image/debian
	docker run --rm --privileged -i deploy-ostree-debian

# combined targets for all Docker versions
qc: qc/debian
