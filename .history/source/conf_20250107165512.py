import os
import sys
sys.path.insert(0, os.path.abspath('..'))
autodoc_mock_imports  = ['MonkAI_agent.setup','MonkAI_agent.config','MonkAI_agent']

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon'
]

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

project = 'MonkAI_agent'
copyright = '2025, MonkAI Team'
author = 'MonkAI Team'
release = 'v.0.0.1'