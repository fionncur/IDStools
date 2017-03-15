
VERSION=$(shell git describe --always --dirty)

# Module imas will set IMAS_HOME to system wide, otherwise pick $PWD/imas:
IMAS_HOME ?= $(realpath $(CURDIR)/$(dir $(lastword $(MAKEFILE_LIST))))/imas

INSTALL = $(IMAS_HOME)/core/imastools/$(VERSION)
INSTALL_MOD = $(IMAS_HOME)/etc/modulefiles/imastools/$(VERSION)
MODULEFILE = module/imastools/$(VERSION)

# Check that python2 and python3 exists and get their full path
PY2:=$(shell command -v python2 2> /dev/null)
PY3:=$(shell command -v python3 2> /dev/null)
PY2VER?=$(shell python2 -c 'print(".".join(str(i) for i in __import__("sys").version_info[:2]))' 2>/dev/null)
PY3VER?=$(shell python3 -c 'print(".".join(str(i) for i in __import__("sys").version_info[:2]))' 2>/dev/null)
INSTALL_PY2 = $(INSTALL)/lib/python$(PY2VER)
INSTALL_PY3 = $(INSTALL)/lib/python$(PY3VER)

install: tools_install module_install
uninstall: tools_uninstall module_uninstall
module : $(MODULEFILE)

clean:
	rm -f imastools/*.pyc
	rm -rf build/
	rm -rf module/imastools/

tools_uninstall:
	rm -rf $(INSTALL)
tools_install: install_deps
	install -d $(INSTALL)
	echo $(VERSION) > $(INSTALL)/VERSION
ifneq (,$(PY2VER))
	install -d $(INSTALL_PY2)
	python2 setup.py install --install-lib=$(INSTALL_PY2) --install-scripts=$(INSTALL)/bin
endif
#ifneq (,$(PY3VER))
#	install -d $(INSTALL_PY3)
#	python3 setup.py install --install-lib=$(INSTALL_PY3) --install-scripts=$(INSTALL)/bin
#endif

module_uninstall:
	rm -f $(INSTALL_MOD)
	rmdir $(dir $(INSTALL_MOD)) || true
module_install: install_deps $(MODULEFILE)
	install -d $(dir $(INSTALL_MOD))
	install $(MODULEFILE) $(INSTALL_MOD)

.PHONY: $(MODULEFILE) install_deps
$(MODULEFILE):  module/imastools.in
	install -d $(dir $@)
	sed -e "s;__VERSION__;$(VERSION);" \
		-e "s;__PY2VER__;$(PY2VER);" \
		-e "s;__IMAS_HOME__;$(IMAS_HOME);" \
		$< > $@
#		-e "s;__PY3VER__;$(PY3VER);" \

install_deps:
	$(if $(wildcard $(IMAS_HOME)),,$(error IMAS_HOME dir was non existent, did you install imas yet? ($(IMAS_HOME))))
	$(if $(wildcard $(PY2))$(wildcard $(PY3)),,$(error No python2 or python3 executable in path, did you load any python module?))
	$(info Using IMAS_HOME: $(IMAS_HOME))
	$(info Found python2: $(PY2))
#	$(info Found python3: $(PY3))

