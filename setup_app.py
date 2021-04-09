"""
This is a setup_app.py script generated by py2applet

Usage:
    python setup_app.py py2app
"""

from setuptools import setup

APP = ['build_csv.py']
DATA_FILES = []
OPTIONS = {}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)