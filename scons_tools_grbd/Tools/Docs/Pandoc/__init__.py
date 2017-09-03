"""
If the user requests "Docs.Mkdocs" then this will call this script as a tool
In which case we include all the Mkdocs related builders
"""

from . import PandocBuild

def generate(env):
    PandocBuild.generate(env)

def exists(env):
    if (PandocBuild.exists(env) == False): return False
    return True
