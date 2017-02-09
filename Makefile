VERSION = R2

INSTALL := $(realpath $(CURDIR)/$(dir $(lastword $(MAKEFILE_LIST))))/dist
# Uncomment the following line for performing system-wide installation
#INSTALL = "$(SWIMASDIR)/imastools/${VERSION}"
INSTALL_PY = "$(INSTALL)/lib/python${PYTHONVERSION}"

#INSTALL_DV = ${INSTALL}/${DATAVERSION}
#INSTALL_PY_DV = "$(INSTALL)/lib/python${PYTHONVERSION}"

install:
	install -d $(INSTALL_PY)
	python setup.py install --install-lib=$(INSTALL_PY) --install-scripts=$(INSTALL)/bin
	svn info > $(INSTALL)/version

clean:
	rm -rf dist build

install-clean:
	rm -rf $(INSTALL)
