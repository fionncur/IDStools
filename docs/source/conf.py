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
import datetime
import json
import os
import re
import sys

root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

sys.path.insert(0, root_path)
import idstools

print(f"root path:{root_path}")
print(f"python exec:{sys.executable}")
print(f"sys.path:{sys.path}")
# -- Project information -----------------------------------------------------

project = "IDStools"
copyright = f"{datetime.datetime.now().year}, ITER Organization"
author = "ITER Organization"

# Get release
release = idstools.__version__

# Get version
versionList = idstools.__version__.split("+")
version = ""
is_develop = False
if len(versionList) == 1:
    version = versionList[0]
if len(versionList) == 2:
    version = f"{versionList[0]}dev"
    is_develop = True

html_context = {"is_develop": is_develop}

print(f"version : {version}, release : {release}")

language = "en"

# {"version": "5.0/index.html#", "title": "5.0", "aliases": ["5.0"]}
switcher_version = ""
if "dev" in version:
    switcher_version = "devdocs"
    version_string = {
        "title": "devdocs",
        "version": "devdocs/index.html#",
        "aliases": ["devdocs"],
    }
else:
    switcher_version = f"{version}"
    version_string = {
        "title": release,
        "version": f"{release}/index.html#",
        "aliases": [release, "latest"],
    }


print(f"release : {release}")
print(f"version_string : {version_string}")

# Open a file in write mode
with open("_static/version.json", "w") as file:
    json.dump(version_string, file)

# -- Intersphinx configuration -----------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html#configuration

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "pandas": ("https://pandas.pydata.org/docs/", None),
    "scipy": ("https://docs.scipy.org/doc/scipy/", None),
    "matplotlib": ("https://matplotlib.org/stable/", None),
}

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "autoapi.extension",
    # "sphinx.ext.autodoc",
    # "sphinx.ext.autosectionlabel",
    "sphinx.ext.todo",
    # "sphinx.ext.githubpages",
    "sphinx.ext.intersphinx",
    # "sphinx.ext.autosummary",
    "sphinx.ext.viewcode",
    # "sphinx.ext.extlinks",
    # "sphinx.ext.graphviz",
    "sphinx.ext.napoleon",
    "sphinx.ext.mathjax",
    # "sphinx_autodoc_typehints",
    # "sphinx_toolbox.collapse",
    # "sphinxcontrib.mermaid",
    "sphinx_immaterial",
    "sphinx_immaterial.apidoc.python.apigen",
    "sphinxcontrib.programoutput",
]

autoapi_dirs = ['../../idstools']
autoapi_type = "python"
autoapi_template_dir = "_templates/autoapi"
autoapi_keep_files = True
autoapi_member_order = 'groupwise'
# Ignore import resolution warnings for dynamically generated modules
autoapi_ignore = ['*/_version.py', '*/test/*']  # _version.py is generated at build time, test modules not documented
autoapi_python_use_implicit_namespaces = True
autoapi_python_class_content = 'both'
autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance",
]

# Configure sphinxcontrib-images
images_config = {
    'default_image_path': '_static/images',
}
# Add any paths that contain templates here, relative to this directory.
# templates_path = ["_templates", sphinx_autosummary_accessors.templates_path]

# The suffix of source filenames.
source_suffix = {
    ".rst": "restructuredtext",
    ".txt": "markdown",
    ".md": "markdown",
}

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build"]

# Suppress warnings for informal/prose type descriptions in docstrings
# These are common when documentation describes return types in prose rather than formal type hints
suppress_warnings = [
    "ref.class",  # Suppress "py:class reference target not found" warnings for informal type descriptions
    "ref.exc",    # Suppress "py:exc reference target not found" for None exceptions
    "ref.meth",   # Suppress "py:meth reference target not found" for informal method references
    "ref.func",   # Suppress "py:func reference target not found" for informal function references
    "ref.obj",    # Suppress "py:obj reference target not found" for external library types like cerberus.Validator
    "autoapi.python_import_resolution",  # Suppress import resolution warnings for dynamically generated modules
    "docutils.attribute",  # Suppress attribute directive errors from autoapi-generated docs
    "docutils.emphasis",  # Suppress emphasis parsing errors in docstrings
]


# -- Extension configuration -------------------------------------------------
# Configuration of sphinx.ext.autodoc
# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html
autodoc_class_signature = "separated"
# autodoc_default_flags = ['members', 'undoc-members']
templates_path = ["_templates"]
# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_immaterial"
# html_favicon = "_static/favicon/favicon_ico.ico"
html_logo = "_static/idstools-48.png"
# html_theme_options = {
#     "logo": {
#         "image_light": "logo.svg",
#         "image_dark": "logo_dark.svg",
#     },
#     "github_url": "https://github.com/numpy/numpy",
#     "collapse_navigation": True,
#     # Add light/dark mode and documentation version switcher:
#     "navbar_end": ["theme-switcher", "version-switcher", "navbar-icon-links"],
# }
html_theme_options = {
    "site_url": "https://sharepoint.iter.org/departments/POP/CM/IMDesign/Code%20Documentation/idstools-doc/latest.html",
    "repo_url": "https://git.iter.org/projects/IMAS/repos/idstools",
    "repo_name": "IDStools",
    "icon": {
        "repo": "fontawesome/brands/bitbucket",
    },
    "features": [
        # "navigation.expand",
        # "navigation.tabs",
        "navigation.sections",
        "navigation.instant",
        # "header.autohide",
        "navigation.top",
        # "navigation.tracking",
        # "search.highlight",
        # "search.share",
        # "toc.integrate",
        "toc.follow",
        "toc.sticky",
        # "content.tabs.link",
        "announce.dismiss",
    ],
    # "toc_title_is_page_title": True,
    # "globaltoc_collapse": True,
    "palette": [
        {
            "media": "(prefers-color-scheme: light)",
            "scheme": "default",
            "primary": "light-green",
            "accent": "light-blue",
            "toggle": {
                "icon": "material/lightbulb-outline",
                "name": "Switch to dark mode",
            },
        },
        {
            "media": "(prefers-color-scheme: dark)",
            "scheme": "slate",
            "primary": "deep-orange",
            "accent": "lime",
            "toggle": {
                "icon": "material/lightbulb",
                "name": "Switch to light mode",
            },
        },
    ],
    "version_dropdown": True,
    "version_json": "../versions.js",
}
# templates_path = ["_templates"]
object_description_options = []

# BEGIN: sphinx_immaterial.apidoc.format_signatures extension options
object_description_options.append(("py:.*", dict(wrap_signatures_with_css=True)))
# END: sphinx_immaterial.apidoc.format_signatures extension options


# html_sidebars = {
#     "**": [
#         "search-field.html",
#         # "sidebar-nav-bs.html",
#         # "sidebar-ethical-ads.html",
#         "globaltoc.html",
#     ]
# }
# ['globaltoc.html', 'sourcelink.html', 'searchbox.html'],
#    'using/windows': ['windowssidebar.html', 'searchbox.html']
# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# The full version, including alpha/beta/rc tags

html_title = f"{project} v{release} Manual"

html_static_path = ["_static"]
# html_css_files = ["idstools.css"]
# html_context = {"default_mode": "light"}
html_file_suffix = ".html"
htmlhelp_basename = "IDStools"

# Configuration of sphinx.ext.autosummary
# https://www.sphinx-doc.org/en/master/usage/extensions/autosummary.html
autosummary_generate = True


# Configuration of sphinx.ext.napoleon
# Support for NumPy and Google style docstrings
# See https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = True
# napoleon_include_special_with_doc = True
# napoleon_use_admonition_for_examples = False
# napoleon_use_admonition_for_notes = False
# napoleon_use_admonition_for_references = False
# napoleon_use_ivar = False
# napoleon_use_param = True
# napoleon_use_keyword = False
# napoleon_use_rtype = True
napoleon_preprocess_types = True
napoleon_type_aliases = {
    # general terms
    "sequence": ":term:`sequence`",
    "iterable": ":term:`iterable`",
    "callable": ":py:func:`callable`",
    "dict_like": ":term:`dict-like <mapping>`",
    "dict-like": ":term:`dict-like <mapping>`",
    "mapping": ":term:`mapping`",
    "file-like": ":term:`file-like <file-like object>`",
    # special terms
    # 'same type as caller': '*same type as caller*',  # does not work, yet
    # 'same type as values': '*same type as values*',  # does not work, yet
    # stdlib type aliases
    "MutableMapping": "~collections.abc.MutableMapping",
    "sys.stdout": ":obj:`sys.stdout`",
    "timedelta": "~datetime.timedelta",
    "string": ":class:`string <str>`",
    # numpy terms
    "array_like": ":term:`array_like`",
    "array-like": ":term:`array-like <array_like>`",
    "scalar": ":term:`scalar`",
    "array": ":term:`array`",
    "hashable": ":term:`hashable <name>`",
    # matplotlib terms
    "color-like": ":py:func:`color-like <matplotlib.colors.is_color_like>`",
    "matplotlib colormap name": ":doc:matplotlib colormap name <Colormap reference>",
    "matplotlib_axes": ":py:class:`matplotlib axes object <matplotlib.axes.Axes>`",
    "colormap": ":py:class:`colormap <matplotlib.colors.Colormap>`",
    # objects without namespace
    "DataArray": "~xarray.DataArray",
    "Dataset": "~xarray.Dataset",
    "Variable": "~xarray.Variable",
    "ndarray": "~numpy.ndarray",
    "MaskedArray": "~numpy.ma.MaskedArray",
    "dtype": "~numpy.dtype",
    "ComplexWarning": "~numpy.ComplexWarning",
    "Index": "~pandas.Index",
    "MultiIndex": "~pandas.MultiIndex",
    "CategoricalIndex": "~pandas.CategoricalIndex",
    "TimedeltaIndex": "~pandas.TimedeltaIndex",
    "DatetimeIndex": "~pandas.DatetimeIndex",
    "Series": "~pandas.Series",
    "DataFrame": "~pandas.DataFrame",
    "Categorical": "~pandas.Categorical",
    "Path": "~~pathlib.Path",
    # objects with abbreviated namespace (from pandas)
    "pd.Index": "~pandas.Index",
    "pd.NaT": "~pandas.NaT",
    "pd.DataFrame": "~pandas.NaT",
}  # TODO: From xarray, improve! New in 3.2

napoleon_attr_annotations = (
    True  # Allow PEP 526 attributes annotations in classes. New in 3.4
)
