from pallets_sphinx_themes import get_version
from pallets_sphinx_themes import ProjectLink

import os
import sys
sys.path.insert(0, os.path.abspath('../pyjaws/pyjaws'))

# Project --------------------------------------------------------------

project = "pyjaws"
author = "pyjaws"
release, version = get_version("pyjaws")

# General --------------------------------------------------------------

master_doc = "index"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinxcontrib.log_cabinet",
    "pallets_sphinx_themes",
    "sphinx_issues",
    "sphinx_tabs.tabs",
    "sphinx.ext.napoleon",
    "myst_parser",
    'sphinx.ext.autosectionlabel'
]
autodoc_typehints = "description"
intersphinx_mapping = {"python": ("https://docs.python.org/3/", None)}

# HTML -----------------------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_theme_path = ["_themes", ]
html_theme_options = {"index_sidebar_logo": False}
html_sidebars = {
    "index": ["project.html", "localtoc.html", "searchbox.html", "ethicalads.html"],
    "**": ["localtoc.html", "relations.html", "searchbox.html", "ethicalads.html"],
}
singlehtml_sidebars = {"index": ["project.html", "localtoc.html", "ethicalads.html"]}
html_static_path = ["_static"]
html_favicon = "_static/click-icon.png"
html_logo = "_static/click-logo-sidebar.png"
html_title = f"PyJaws Documentation ({version})"
html_show_sourcelink = True
html_extra_path = ["_html/robots.txt", "_html/googled37ca91719e87a84.html"]

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = True
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True

add_module_names = True
myst_html_meta = {
    "description lang-en": "test123"
}