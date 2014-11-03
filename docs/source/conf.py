# -*- coding: utf-8 -*-

import sys
import os

sys.path.insert(0, os.path.abspath("../.."))

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
]

templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = u'PandaSurvey'
copyright = u'2014, InContext Solutions'
version = '0.100'
release = '0.100'
exclude_patterns = []
pygments_style = 'sphinx'

import sphinx_rtd_theme
html_theme = "sphinx_rtd_theme"
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

html_static_path = ['_static']
htmlhelp_basename = 'PandaSurveydoc'
