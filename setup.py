# -*- coding: utf-8 -*-
"""
Created on Fri Sep 26 21:10:27 2014

@author: robert.w.smith08@gmail.com
"""

from distutils.core import setup
import os

def is_package(path):
    return (
        os.path.isdir(path) and
        os.path.isfile(os.path.join(path, '__init__.py'))
        )

def find_packages(path, base=""):
    """ Find all packages in path """
    packages = {}
    for item in os.listdir(path):
        dir = os.path.join(path, item)
        if is_package( dir ):
            if base:
                module_name = "%(base)s.%(item)s" % vars()
            else:
                module_name = item
            packages[module_name] = dir
            packages.update(find_packages(dir, module_name))
    return packages


my_packages = find_packages('.')

setup(
    name = 'utilities',
    package_dir = my_packages,
    packages = my_packages.keys(),
    version = "0.0.1",
    description = "Data Analysis Utilities",
    author = "Robert Smith",
    author_email = "robert.w.smith08@gmail.com",
    url = "http://localhost:8080"
    )
