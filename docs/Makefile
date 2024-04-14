# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source
GENERATEDDIR  = $(SOURCEDIR)/generated
BUILDDIR      = _build
PROJECT_ROOT  = ..
# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
html: Makefile autogen
	rst2pdf "$(SOURCEDIR)"/cheatsheet.rst --output="$(SOURCEDIR)"/_static/cheatsheet.pdf
	@echo Running '$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)'
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O) -T
	
man: Makefile
	@echo Running '$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)'
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O) -T

clean: Makefile
	@echo Running '$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)'
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	
# apidocs: Makefile
#	sphinx-apidoc -f -d 6 --separate --implicit-namespaces -o "$(GENERATEDDIR)" "$(PROJECT_ROOT)/idstools/"

# Sphinx will run this automatically
autogen: Makefile
	sphinx-autogen -o "$(GENERATEDDIR)" $(SOURCEDIR)/*.rst

realclean: Makefile clean
	rm -rf $(GENERATEDDIR) $(SOURCEDIR)/_build/
