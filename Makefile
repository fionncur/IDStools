
VERSION = $(shell git describe --always --dirty)
export PKGVERSION = $(shell echo $(VERSION) | awk 'BEGIN{FS="-"} ; {if (NF >= 3) if ($$2>0) print $$1".dev"$$2"+"$$3$$4; else print $$1"+"$$3$$4; else print $$1}')

# Inherit a site-config where you can override defaults.
# Choose your site configuration file manually, e.g.
#SITECONFIG=./site-config/Makefile.ITER.HPC
# Or let the hostname/OS determine the appropriate:
ifndef SITECONFIG
SITECONFIG:=$(shell imas-config-installer)
endif
ifeq (,$(wildcard $(SITECONFIG)))
$(error Error in finding site-config, load imas module or try setting SITECONFIG=./site-config/Makefile.default)
endif
include $(SITECONFIG)

# Module imas will set IMAS_HOME to system wide, otherwise pick $PWD/imas:
IMAS_HOME ?= $(realpath $(CURDIR)/$(dir $(lastword $(MAKEFILE_LIST))))/imas
IDSTOOLS_NAME ?= idstools

INSTALL = $(IMAS_HOME)/core/$(IDSTOOLS_NAME)/$(VERSION)
INSTALL_MOD = $(IMAS_HOME)/etc/modulefiles/$(IDSTOOLS_NAME)/$(VERSION)
MODULEFILE = module/$(IDSTOOLS_NAME)/$(VERSION)

# Check that python2 and python3 exists and get their full path
PY2:=$(shell command -v python2 2> /dev/null)
PY3:=$(shell command -v python3 2> /dev/null)
PY2VER?=$(shell python2 -c 'print(".".join(str(i) for i in __import__("sys").version_info[:2]))' 2>/dev/null)
PY3VER?=$(shell python3 -c 'print(".".join(str(i) for i in __import__("sys").version_info[:2]))' 2>/dev/null)
INSTALL_PY2 = $(INSTALL)/lib/python$(PY2VER)
INSTALL_PY3 = $(INSTALL)/lib/python$(PY3VER)

all: tools_build module
install: tools_install module_install
uninstall: tools_uninstall module_uninstall
module : $(MODULEFILE)

clean:
	rm -f idstools/*.pyc
	rm -rf build/
	rm -rf module/$(IDSTOOLS_NAME)/

tools_build:
ifneq (,$(PY2VER))
	python2 setup.py build -e '/usr/bin/env python'
endif
ifneq (,$(PY3VER))
	python3 setup.py build -e '/usr/bin/env python'
endif


tools_uninstall:
	rm -rf $(INSTALL)
tools_install: install_deps tools_build
	install -d $(INSTALL)
ifneq (,$(PY2VER))
	install -d $(INSTALL_PY2)
	python2 setup.py install --install-lib=$(INSTALL_PY2) --install-scripts=$(INSTALL)/bin
endif
ifneq (,$(PY3VER))
	install -d $(INSTALL_PY3)
	python3 setup.py install --install-lib=$(INSTALL_PY3) --install-scripts=$(INSTALL)/bin
endif

module_uninstall:
	rm -f $(INSTALL_MOD)
	rmdir $(dir $(INSTALL_MOD)) || true
module_install: install_deps $(MODULEFILE)
	install -d $(dir $(INSTALL_MOD))
	install $(MODULEFILE) $(INSTALL_MOD)

.PHONY: $(MODULEFILE) install_deps
$(MODULEFILE):  module/idstools.in
	install -d $(dir $@)
	sed -e "s;__VERSION__;$(VERSION);" \
		-e "s;__PY2VER__;$(PY2VER);" \
		-e "s;__PY3VER__;$(PY3VER);" \
		-e "s;__IMAS_HOME__;$(IMAS_HOME);" \
		-e "s;__IMAS_MODULE__;$(IMAS_MODULE);" \
		-e "s;__IDSTOOLS_NAME__;$(IDSTOOLS_NAME);" \
		$< > $@

install_deps:
	$(if $(wildcard $(IMAS_HOME)),,$(error IMAS_HOME dir was non existent, did you install imas yet? ($(IMAS_HOME))))
	$(if $(wildcard $(PY2))$(wildcard $(PY3)),,$(error No python2 or python3 executable in path, did you load any python module?))
	$(info Using IMAS_HOME: $(IMAS_HOME))
	$(info Found python2: $(PY2))
	$(info Found python3: $(PY3))

