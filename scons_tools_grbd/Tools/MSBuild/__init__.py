"""
If the user requests "MSBuild" then this will call this script as a tool
In which case we include all the related builders
"""

from . import DotnetCore, VC

def generate(env):
    DotnetCore.generate(env)
    VC.generate(env)

def exists(env):
    if (DotnetCore.exists(env) == False): return False
    if (VC.exists(env) == False): return False
    return True
