IMAGE_TAG := deploy-ostree:latest
SRC_DIR := $(PWD)

ifeq ($(OS),Windows_NT)
	PYTHON := py -3
else
	PYTHON := python3
endif

LOCAL_UNITTEST := $(PYTHON) -m unittest discover -v -t . -s

DOCKER_UNITTEST := docker run --rm -i --privileged -v /ostree -v $(SRC_DIR)/tests:/tests $(IMAGE_TAG) python3 -m unittest discover -v -t / -s

all: lint test/unit test/provisioners build/docker build/wheel test/integration test/integration_long

lint:
	flake8 .
	mypy .

test/unit:
	$(LOCAL_UNITTEST) tests/unit

test/provisioners:
	$(LOCAL_UNITTEST) tests/provisioners

build/docker:
	docker build -t $(IMAGE_TAG) .

build/wheel:
	$(PYTHON) setup.py bdist_wheel

test/integration:
	$(DOCKER_UNITTEST) tests/integration

test/integration_long:
	$(DOCKER_UNITTEST) tests/integration_long
