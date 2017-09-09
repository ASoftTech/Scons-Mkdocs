"""
If the user requests "Docs.Doxygen" then this will call this script as a tool
In which case we include all the Doxygen related builders
"""

from . import Doxygen, DoxygenDefaultTemplate

def generate(env):
    Doxygen.generate(env)
    DoxygenDefaultTemplate.generate(env)

def exists(env):
    if (Doxygen.exists(env) == False): return False
    if (DoxygenDefaultTemplate.exists(env) == False): return False
    return True
