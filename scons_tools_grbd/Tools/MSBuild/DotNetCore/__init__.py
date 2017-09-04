"""
If the user requests "MSBuild.DotNetCore" then this will call this script as a tool
In which case we include all the related builders
"""

#from . import Dll2Lib

def generate(env):
    # TODO
    #Dll2Lib.generate(env)
    pass

def exists(env):
    # TODO
    #if (Dll2Lib.exists(env) == False): return False
    return True
