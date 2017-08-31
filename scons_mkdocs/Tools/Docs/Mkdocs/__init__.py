"""
If the user requests "Docs.Mkdocs" then this will call this script as a tool
In which case we include all the Mkdocs related builders
Note MkdocsRunner is not a scons builder but a Class the other Builders use in common
"""

from . import MkdocsServer, MkdocsBuild, MkdocsJsonBuild, MkdocsPublish, MkdocsPandoc, MkdocsDoxyTemplate

def generate(env):
    MkdocsServer.generate(env)
    MkdocsBuild.generate(env)
    MkdocsJsonBuild.generate(env)
    MkdocsPublish.generate(env)
    MkdocsPandoc.generate(env)

    MkdocsDoxyTemplate.generate(env)

def exists(env):
    if (MkdocsServer.exists(env) == False): return False
    if (MkdocsBuild.exists(env) == False): return False
    if (MkdocsJsonBuild.exists(env) == False): return False
    if (MkdocsPublish.exists(env) == False): return False
    if (MkdocsPandoc.exists(env) == False): return False

    if (MkdocsDoxyTemplate.exists(env) == False): return False
    return True
