"""
If the user requests "MSBuild.VC" then this will call this script as a tool
In which case we include all the related builders
"""

from . import Util

def generate(env):
    Util.generate(env)

def exists(env):
    if (Util.exists(env) == False): return False
    return True
