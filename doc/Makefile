# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

update_web: clean-src html 
	# make html
	rsync --delete -rv _build/html/* ~/Trabajos/fiolj-github/sparta/
	# cp _build/latex/sparta.pdf ~/trabajo/Proyectos/fiolj-github/data/sparta-manual.pdf
	# cp _build/epub/SPARTA.epub ~/trabajo/Proyectos/fiolj-github/data/sparta-manual.epub

clean-src:
	rm -f *.rst~
