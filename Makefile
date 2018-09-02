SRC_DIR := $(PWD)

ifeq ($(OS),Windows_NT)
	PYTHON := py -3
else
	PYTHON := python3
endif

all: lint test/unit test/provisioners build/wheel build/docker test/integration test/integration_long

# local checks
LOCAL_UNITTEST := $(PYTHON) -m unittest discover -v -t $(SRC_DIR) -s

lint:
	flake8 $(SRC_DIR)
	mypy $(SRC_DIR)

test/unit:
	$(LOCAL_UNITTEST) tests/unit

test/provisioners:
	$(LOCAL_UNITTEST) tests/provisioners

build/wheel:
	-rm -f dist/*.whl
	$(PYTHON) setup.py bdist_wheel

# dockerized tests
IMAGE_TAG := deploy-ostree
DOCKER_UNITTEST := docker run --rm -i --privileged -v /ostree -v $(SRC_DIR)/tests:/tests $(IMAGE_TAG) python3 -m unittest discover -v -t / -s

build/docker:
	docker build -t $(IMAGE_TAG) --build-arg PACKAGE=$(shell ls -1 dist/*.whl | xargs basename) .

test/integration:
	$(DOCKER_UNITTEST) tests/integration

test/integration_long:
	$(DOCKER_UNITTEST) tests/integration_long

# cleanup
clean:
	-rm -rf dist/*.whl
	-docker image rm $(IMAGE_TAG)
