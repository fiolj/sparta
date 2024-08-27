# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

# -- Path setup --------------------------------------------------------------
from datetime import date
today = date.today().strftime("%d/%m/%Y")

# -- Project information -----------------------------------------------------

project = f'SPARTA  ({format(today)})'
copyright = date.today().strftime("%Y")
author = 'SPARTA'

# The full version, including alpha/beta/rc tags
# release = '26 Feb 2021'
release = ''

version = release + "  (build: {})".format(today)

# -- General configuration ---------------------------------------------------
master_doc = 'index'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = []

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']
language = 'en'
# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# pygments_style = 'sphinx'
pygments_style = 'emacs'
# pygments_style = 'autumn'
# pygments_style = NO: 'monokai', 'fruity', 'vim', 'native', "solarized-dark", 'solarized-light', 'paraiso-dark', 'stata', 'stata-light', 'stata-dark'
# pygments_style = 'colorful'
# pygments_style = 'manni'
# pygments_style = 'paraiso-light'
# pygments_style = 'rainbow_dash'


# def pygments_monkeypatch_lexer(mod_name, lexer):
#   import sys
#   import pygments.lexer
#   # mod = 'Sparta'
#   lexer_name = "Sparta"
#   # cls_name = cls.__name__
#   mod = type(__import__("os"))(mod_name)
#   print('Mod:', mod)
#   setattr(mod, lexer_name, SpartaLexer)
#   setattr(pygments.lexer, mod_name, mod)
#   sys.modules["pygments.lexer." + mod_name] = mod
#   # from pygments.lexers._mapping import LEXERS
#   # s = ('.sparta_hg', lexer.name,
#   #      tuple(lexer.aliases),
#   #      tuple(lexer.filenames),
#   #      tuple(lexer.mimetypes))
#   # LEXERS['SpartaLexer'] = s
# # pygments_monkeypatch_lexer("Sparta", SpartaLexer)

highlight_language = "xorg.conf"
# highlight_language = "sparta"

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'
html_css_files = [
    'rtd_overrides.css',
    'pygm_overrides.css'
]
html_static_path = ['_static']

# OPTIONS FOR EPUB

epub_publisher = "J.F."
epub_use_index = True


# LATEX OPTIONS

latex_elements = {'preamble': r"""
\usepackage{enumitem}

\hypersetup{pdfborder={0 0 0}, pdftitle={SPARTA Manual},
  pdfsubject={DSMC},
  pdfpagemode={UseOutlines},
  pdfhighlight  =/P,
}
"""}
