"""
If the user requests "MSBuild.DotnetCore" then this will call this script as a tool
In which case we include all the related builders
"""

from . import DotnetCoreBuild

def generate(env):
    DotnetCoreBuild.generate(env)
    pass

def exists(env):
    if (DotnetCoreBuild.exists(env) == False): return False
    return True
