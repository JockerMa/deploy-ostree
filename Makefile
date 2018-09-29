ifeq ($(OS),Windows_NT)
	PYTHON := py -3
else
	PYTHON := python3
endif

all: lint test/unit test/provisioners build/wheel build/docker test/integration test/integration_long

# local checks
build:
	mkdir -p build

lint: build
	flake8 .
	mypy .

test/unit:
	pytest tests/unit

test/provisioners:
	pytest tests/builtin_provisioners

# package
build/wheel: clean/wheels
	$(PYTHON) setup.py bdist_wheel

test/check-wheel:
	twine check dist/*

# dockerized tests
IMAGE_TAG := deploy-ostree
WORKDIR := $(shell pwd)

build/docker:
	docker build -t $(IMAGE_TAG) --build-arg PACKAGE=$(shell ls -1 dist/*.whl | xargs basename) .

define docker_test
	docker run --rm -i \
		--privileged \
		--volume /ostree \
		--volume /tmp/deploy-ostree.test/sysroot \
		--volume $(WORKDIR):$(WORKDIR) \
		--workdir $(WORKDIR) \
		$(IMAGE_TAG) \
		$(1)
endef

test/isolated: build/docker
	$(call docker_test, pytest $(TEST))

test/integration: build/docker
	$(call docker_test, pytest tests/integration -m "not slow")

test/integration_slow: build/docker
	$(call docker_test, pytest tests/integration -m "slow")

# push to PyPI
release/test:
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*.whl

release/pypi:
	twine upload --repository-url https://upload.pypi.org/legacy/ dist/*.whl

# cleanup
clean: clean/wheels
	-find . -name "*.pyc" -delete
	-rm -rf build
	-docker image rm -f $(IMAGE_TAG)

clean/wheels:
	-rm -rf dist/*.whl
