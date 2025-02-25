# __init__.py
# This file can be empty.
# It is used to tell Python that this directory should be treated as a package.
# This allows us to import modules from this directory in other files.
# Why empty?
# We're using gui as a simple organizational package.
# We don't need any package-level initialization or to make specific modules/functions directly accessible under the gui namespace.
# app.py imports the individual modules (e.g., from gui.homepage import render_homepage) explicitly.