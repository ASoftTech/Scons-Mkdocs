"""
If the user requests "Docs.Mkdocs" then this will call this script as a tool
In which case we include all the Mkdocs related builders
Note MkdocsRunner is not a scons builder but a Class the other Builders use in common
"""

from . import MkdocsBuilder, MkdocsPublisher, MkdocsServer, MkdocsDoxyTemplate

def generate(env):
    MkdocsBuilder.generate(env)
    MkdocsPublisher.generate(env)
    MkdocsServer.generate(env)
    MkdocsDoxyTemplate.generate(env)

def exists(env):
    if (MkdocsBuilder.exists(env) == False): return False
    if (MkdocsPublisher.exists(env) == False): return False
    if (MkdocsServer.exists(env) == False): return False
    if (MkdocsDoxyTemplate.exists(env) == False): return False
    return True
