DOCKER = $(patsubst %/Makefile,%,$(shell find docker -mindepth 2 -name Makefile))
DOCKER_PULL = $(patsubst %,%-pull,$(DOCKER))
DOCKER_OPTS ?= 

VIRTUALENV ?= virtualenv
PYTHON_ENV = $(shell test -d "venv" && echo "venv/bin/" || true)
PYTHON ?= python

.PHONY: clean install all docker docker-pull $(DOCKER) $(DOCKER_PULL)

all: dist

clean:
	rm -Rf venv ansibleroletest/*.pyc build ansible_role_test.egg-info

install:
	$(PYTHON_ENV)$(PYTHON) setup.py install

# same as build but use symbolic links
dev: venv
	venv/bin/pip install --upgrade -e .

venv:
	$(VIRTUALENV) --python=$(PYTHON) venv

# build the necessary docker images
docker: $(DOCKER)

docker-pull: $(DOCKER_PULL)

$(DOCKER):
	make -C $@

$(DOCKER_PULL):
	DOCKER_OPTS="$(DOCKER_OPTS)" make -C $(patsubst %-pull,%,$@) pull

fresh:
	$(shell docker ps    | tail -n+2 | awk '{print $$1}' | xargs docker kill >/dev/null 2>&1 || true )
	$(shell docker ps -a | tail -n+2 | awk '{print $$1}' | xargs docker rm >/dev/null 2>&1 || true )
	$(shell docker images | grep failed | awk '{print $$1,":",$$2}' | sed 's/ //g' | xargs docker rmi >/dev/null 2>&1 || true )
	$(shell docker images | grep successful | awk '{print $$1,":",$$2}' | sed 's/ //g' | xargs docker rmi >/dev/null 2>&1 || true )
