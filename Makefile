VERSION := 1.0.0
SRC_DIR := $(PWD)

ifeq ($(OS),Windows_NT)
	PYTHON := py -3
else
	PYTHON := python3
endif

all: lint test/unit test/provisioners build/wheel test/integration test/integration_long

# local checks
LOCAL_UNITTEST := $(PYTHON) -m unittest discover -v -t $(SRC_DIR) -s

lint:
	flake8 $(SRC_DIR)
	mypy $(SRC_DIR)

test/unit:
	$(LOCAL_UNITTEST) tests/unit

test/provisioners:
	$(LOCAL_UNITTEST) tests/provisioners

# package
PACKAGE := deploy_ostree-$(VERSION)-py3-none-any.whl

build/wheel: dist/$(PACKAGE)
dist/$(PACKAGE): export DEPLOY_OSTREE_VERSION=$(VERSION)
dist/$(PACKAGE):
	$(PYTHON) setup.py bdist_wheel

# dockerized tests
IMAGE_TAG := deploy-ostree
DOCKER_UNITTEST := docker run --rm -i --privileged -v /ostree -v $(SRC_DIR)/tests:/tests $(IMAGE_TAG) python3 -m unittest discover -v -t / -s

build/docker: dist/$(PACKAGE)
	docker build -t $(IMAGE_TAG) --build-arg PACKAGE=$(PACKAGE) .

test/integration: build/docker
	$(DOCKER_UNITTEST) tests/integration

test/integration_long: build/docker
	$(DOCKER_UNITTEST) tests/integration_long

# cleanup
clean:
	-rm -rf dist/*.whl
	-docker image rm $(IMAGE_TAG)
