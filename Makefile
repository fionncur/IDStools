# Get version from git, unless .version file is found
VERSION := $(if $(wildcard .version),$(shell cat .version),$(shell git describe --dirty))

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

# Module imas usually sets IMAS_HOME, otherwise pick ~/imas:
IMAS_HOME ?= $(HOME)/imas
IDSTOOLS_NAME ?= IDStools

# Check that python exists and get their full path
PYTHONCMD?=python
PYCMD:=$(if $(PYTHONCMD),$(shell command -v $(PYTHONCMD) 2>/dev/null))
PYVER:=$(if $(PYCMD),$(shell $(PYCMD) -c 'print(".".join(str(i) for i in __import__("sys").version_info[:2]))' 2>/dev/null))

# Installation paths
INSTALL_PREFIX?=$(IMAS_HOME)/core/$(IDSTOOLS_NAME)/$(VERSION)
INSTALL_PY?=$(INSTALL_PREFIX)/lib/python$(PYVER)
INSTALL_MOD?=$(IMAS_HOME)/etc/modulefiles
MODULEFILE?=$(IDSTOOLS_NAME)/$(VERSION)

all: tools_build module
install: tools_install module_install
uninstall: tools_uninstall module_uninstall
module : $(MODULEFILE)

help:
	@echo "Usage: Run 'make all' to build. Run 'make install' to install."
	@echo "Do this for each python installation."
	@echo "Use the following flags to configure the build/install, which you can set on the"
	@echo "command line, in environment or in current SITECONFIG. [$(SITECONFIG)]"
	@echo "PYTHONCMD       Override default python cmd, e.g. python3. [$(PYTHONCMD)]"
	@echo "INSTALL_PREFIX  Where to install. [$(INSTALL_PREFIX)]"
	@echo "INSTALL_PY      Where to install python module. [$(INSTALL_PY)]"
	@echo "INSTALL_MOD     Where to install env module. [$(INSTALL_MOD)]"
	@echo "MODULEFILE      Environment module file. [$(MODULEFILE)]"
	@echo "IDSTOOLS_NAME   Name of the package. [$(IDSTOOLS_NAME)]"
	@echo "VERSION         Version of the package (from .version file or git describe). [$(VERSION)]"

clean:
	rm -f idstools/*.pyc
	rm -rf build/
	rm -rf module/$(IDSTOOLS_NAME)/

tools_build: | tools_deps
	$(PYCMD) setup.py build -e '/usr/bin/env python'
tools_install: tools_build
	install -d $(INSTALL_PREFIX)
	install -d $(INSTALL_PY)
	$(PYCMD) -m pip install --compile --prefix $(INSTALL_PREFIX) .
	@echo "Byte-compiling installed module..."
	PYTHONPATH=$(INSTALL_PY):$$PYTHONPATH $(PYCMD) -c "import idstools"
	make -C dummy_generators INSTALL_DIR=$(INSTALL_PREFIX) install

tools_uninstall:
	rm -rf $(INSTALL_PREFIX)

module_uninstall:
	rm -f $(INSTALL_MOD)/$(MODULEFILE)
	rmdir -p $(dir $(INSTALL_MOD))

module_install: module/$(MODULEFILE) | install_deps
	install -d $(dir $(INSTALL_MOD)/$(MODULEFILE))
	install $< $(INSTALL_MOD)/$(MODULEFILE)

.PHONY: $(MODULEFILE) tools_deps install_deps
module/$(MODULEFILE):  module/IDStools.in
	install -d $(dir $@)
	sed -e "s;__VERSION__;$(VERSION);" \
		-e "s;__PYVER__;$(PYVER);" \
		-e "s;__INSTALL_PREFIX__;$(INSTALL_PREFIX);" \
		-e "s;__INSTALL_PY__;$(INSTALL_PY);" \
		-e "s;__IMAS_MODULE__;$(IMAS_MODULE);" \
		-e "s;__IDSTOOLS_NAME__;$(IDSTOOLS_NAME);" \
		$< > $@

tools_deps:
	$(if $(wildcard $(PYCMD)),,$(error No $(PYTHONCMD) ($$PYTHONCMD) executable found in path, did you load any python module?))

install_deps: tools_deps
	$(if $(wildcard $(IMAS_HOME)),,$(error IMAS_HOME dir was non existent, did you install imas yet? ($(IMAS_HOME))))
	$(if $(VERBOSE),$(info Using SITECONFIG: $(SITECONFIG)))
	$(if $(VERBOSE),$(info Using IMAS_HOME: $(IMAS_HOME)))

