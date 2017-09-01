"""
If the user requests "Docs" then this will call this script as a tool
In which case we include all the documentation related builders
"""

from . import Mkdocs

def generate(env):
    Mkdocs.generate(env)

def exists(env):
    if (Mkdocs.exists(env) == False): return False
    return True
