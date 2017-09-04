"""
If the user requests "MSBuild.VC.Util" then this will call this script as a tool
In which case we include all the related builders
"""

from . import Dll2Lib

def generate(env):
    Dll2Lib.generate(env)

def exists(env):
    if (Dll2Lib.exists(env) == False): return False
    return True
