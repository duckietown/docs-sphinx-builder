# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# http://www.sphinx-doc.org/en/master/config
#
# This file is highly customized to work only with the standard Duckietown repository structure.

import os
import os.path
import sys
import yaml
import tempfile
from shutil import copyfile

######################################################################################################################
#
#    This part creates a temporary module in a temporary folder that contains all
#    node classes in the repo. This is necessary for the autodocs functionality as it
#    works well only with Python modules. These node classes can then be used as `nodes.SomeNode`.
#
######################################################################################################################

module_name = 'nodes'

# Create the temporary module dir
dirpath = tempfile.mkdtemp()
module_dir = os.path.join(dirpath, module_name)
os.makedirs(module_dir)

print("LOOKING FOR NODE SOURCE FILES")
# Find all the nodes and move them to the temp module folder
node_source_files = []
for pkg in os.listdir(os.path.abspath('../../packages/')):
    if '%s.rst' % pkg not in os.listdir(os.path.abspath('packages/')):
        print("WARNING: Package %s doesn't have a corresponding file in docs/packages! Skipping it." % pkg)
        continue
    # Add the include paths such that all the include modules can also be used with autodocs
    sys.path.insert(0, os.path.abspath('../../packages/%s/include' % pkg))
    if os.path.isdir(os.path.abspath('../../packages/%s/src' % pkg)):
        for node_source_file in os.listdir(os.path.abspath('../../packages/%s/src' % pkg)):
            if node_source_file[-3:] == '.py' and node_source_file != '__init__.py':
                node_source_files.append('../../packages/%s/src/%s' % (pkg, node_source_file))
                copyfile('../../packages/%s/src/%s' % (pkg, node_source_file),
                         os.path.join(module_dir, node_source_file))

# Create an __init__.py file for the temporary module
with open(os.path.join(module_dir, '__init__.py'), 'w') as init_file:
    for node_source_file in node_source_files:
        init_file.write('from .%s import *\n' % (node_source_file.split('/')[-1][:-3]))

# Add the temporary module to the paths
sys.path.insert(0, dirpath)
print("Final system path directories:")
print(sys.path)
sys.setrecursionlimit(1500)


######################################################################################################################
#
#    Load the project-specific configuration file and set some basic variables
#
######################################################################################################################

with open("docs_config.yaml", 'r') as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print("ERROR LOADING docs_config.yaml: %s" % exc)
        exit()

# Check that the version of the config file is compatible with this script
supported_version = 'v1'
if not config["docs_config_version"]:
    print("ERROR: version field not in docs_config.yaml!")
    exit()
elif config["docs_config_version"] != supported_version:
    print("ERROR: only version %s of docs_config.yaml files supported!" % supported_version)
    exit()

project = config.get('project', 'Project Name')
copyright = config.get('copyright', 'Duckietown')
author = config.get('author', 'Duck Quackermann')

# The full version, including alpha/beta/rc tags
version = config.get('version', 'version')
release = version

# Add any paths that contain templates here, relative to this directory.
# templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# Set the index page
master_doc = 'index'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

######################################################################################################################
#
#    Setup the napoleon and autodoc extensions
#
######################################################################################################################

# Napoleon (for Google-style docstrings)
extensions = ['sphinxcontrib.napoleon']

# Autodocs
extensions += ['sphinx.ext.autodoc']

# Load all the necesary mock imports
if os.path.isfile('mock_imports'):
    with open('mock_imports') as f:
        autodoc_mock_imports = f.readlines()
    for idx in range(len(autodoc_mock_imports)):
        autodoc_mock_imports[idx] = autodoc_mock_imports[idx].strip(' ').strip('\n')
else:
    print("WARNING: The mock_imports file was not found. No mocking done!")

# Appearance settings
autodoc_default_flags_default = {'members': True,
                                 'member-order': 'alphabetical',
                                 'undoc-members': True,
                                 'inherited-members': True,
                                 'show-inheritance': True}
autodoc_default_flags = config.get('autodoc_default_flags', autodoc_default_flags_default)
add_module_names = config.get('add_module_names', False)

# Napoleon settings
napoleon_google_docstring = config.get('napoleon_google_docstring', True)
napoleon_numpy_docstring = config.get('napoleon_numpy_docstring', False)
napoleon_include_init_with_doc = config.get('napoleon_include_init_with_doc', False)
napoleon_include_private_with_doc = config.get('napoleon_include_private_with_doc', False)
napoleon_include_special_with_doc = config.get('napoleon_include_special_with_doc', False)
napoleon_use_admonition_for_examples = config.get('napoleon_use_admonition_for_examples', True)
napoleon_use_admonition_for_notes = config.get('napoleon_use_admonition_for_notes', True)
napoleon_use_admonition_for_references = config.get('napoleon_use_admonition_for_references', True)
napoleon_use_ivar = config.get('napoleon_use_ivar', False)
napoleon_use_param = config.get('napoleon_use_param', False)
napoleon_use_rtype = config.get('napoleon_use_rtype', True)
napoleon_use_keyword = config.get('napoleon_use_keyword', True)

napoleon_custom_section = [(sec_name, 'Parameters') for sec_name in config.get('custom_sections', [])]


######################################################################################################################
#
#    Settings for the theme
#
######################################################################################################################

html_theme = 'sphinx_rtd_theme'
html_theme_options_default = {
    # 'canonical_url': '',
    # 'analytics_id': 'UA-XXXXXXX-1',  #  Provided by Google in your dashboard
    # 'logo_only': False,
    # 'display_version': True,
    'prev_next_buttons_location': 'bottom',
    # 'style_external_links': False,
    # 'vcs_pageview_mode': '',
    'style_nav_header_background': '#fbc10b',
    # Toc options
    'collapse_navigation': False,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': False,
    'titles_only': False,
    # 'github_url': True
}

html_theme_options = config.get('html_theme_options', html_theme_options_default)
html_logo = config.get('html_logo', 'default_logo.png')
html_favicon = config.get('html_favicon', 'default_favicon.png')


