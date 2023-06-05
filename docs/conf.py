# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('../lsdo_project_template/core'))


# -- Project information -----------------------------------------------------

project = 'lsdo_project_template'
copyright = '2022, anugrah'
author = 'anugrah'
version = '0.1'
# release = 0.1.0rtc


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
# extensions = ["sphinx.ext.autodoc"]
extensions = [
    "autoapi.extension", # autoapi is not needed when using autodoc
    # "sphinx.ext.autodoc",
    # "sphinx.ext.napoleon", # another extension to read numpydoc style but 'numpydoc' extension looks better
    "numpydoc", # numpydoc already includes autodoc
    # "myst_parser", # compiles .md, .myst files
    "myst_nb", # compiles .md, .myst, .ipynb files
    "sphinx.ext.viewcode"
]
autoapi_dirs = ["../lsdo_project_template/core"]

root_doc = 'index'

# source_suffix = {
#     '.rst': 'restructuredtext',
#     # '.md': 'markdown',
#     # '.ipynb': 'Jupyter notebook',
#     }

# # source_parsers = {'.md': 'myst_nb',
# #                 '.ipynb': 'myst_nb',
# #                 }

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = 'alabaster'
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ['_static']


# extensions = [
#     "myst_nb",
#     "autoapi.extension",
#     "sphinx.ext.napoleon",
#     "sphinx.ext.viewcode",
# ]
# autoapi_dirs = ["../src"]
