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
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))
import sphinx_rtd_theme

# sys.path.insert(0, os.path.abspath('..'))  # Source code dir relative to this file

# -- Project information -----------------------------------------------------

project = 'LexicalRichness'
copyright = '2023, Lucas Shen'
author = 'Lucas Shen'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
	'sphinx_rtd_theme',
	'sphinx.ext.autodoc',
	'sphinx.ext.duration',
	'sphinx.ext.napoleon',
    'sphinx_copybutton',
	'nbsphinx',
]

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
html_theme = 'sphinx_material'
# html_theme = 'sphinx_rtd_theme'

# Material theme options (see theme.conf for more information)
html_theme_options = {
    # Set the name of the project to appear in the navigation.
    'nav_title': 'LexicalRichness',

    # Set the repo location to get a badge with stats
    'repo_url': 'https://github.com/lsys/LexicalRichness',
    'repo_name': 'LexicalRichness',
    'repo_type': 'github',

    # Visible levels of the global TOC; -1 means unlimited
    'globaltoc_depth': 1,
    # If False, expand all TOC entries
    'globaltoc_collapse': False,
    # If True, show hidden TOC entries
    'globaltoc_includehidden': False,
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# You must explicitly include globaltoc.html in html_sidebars if you want the toc to show up.
# https://bashtage.github.io/sphinx-material/customization.html#sidebars
html_sidebars = {
    "**": [
    "logo-text.html", 
    "globaltoc.html", 
    "localtoc.html", 
    "searchbox.html",
    ]
}