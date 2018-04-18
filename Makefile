ifeq ($(OS),Windows_NT)
	PYTHON := py -3
else
	PYTHON := python3
endif

UNITTEST := $(PYTHON) -m unittest discover -v -t . -s

dummy:
	@echo please select a target explicitly

# plain linting/test targets
lint:
	flake8 .
	mypy . \
		--ignore-missing-imports \
		--check-untyped-defs

test/unit:
	$(UNITTEST) tests/unit

test/provisioners:
	$(UNITTEST) tests/provisioners

test/integration:
	$(UNITTEST) tests/integration

test: test/unit test/provisioners test/integration

qc/host: lint test

# Debian
image/debian:
	docker build -t deploy-ostree-debian -f Dockerfile.debian .

qc/debian: image/debian
	docker run --rm --privileged -i -v /ostree deploy-ostree-debian

# combined targets for all Docker versions
qc: qc/debian
