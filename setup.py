'''
Created on 12 Mar 2012

@author: Daniel Kershaw
'''
from distutils.core import setup
#import py2exe

files = ["main/*"]

setup(name = "Project N-Fly",
    version = "0.1",
    description = "NLP Keyword Extraction of Online Content for an Online Advertising Systems",
    author = "Daniel Kershaw",
    author_email = "d.kershaw1@lancaster.ac.uk",
    url = "http://github.com/danjamker/N-Fly",
    long_description = """Really long text here.""",
    py_modules = ['main\main.py']
) 