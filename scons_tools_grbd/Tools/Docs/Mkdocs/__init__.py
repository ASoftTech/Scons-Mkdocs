"""
If the user requests "Docs.Mkdocs" then this will call this script as a tool
In which case we include all the Mkdocs related builders
"""

from . import MkdocsServer, MkdocsBuild, MkdocsJsonBuild, MkdocsPublish, Mkdocs2Pandoc, MkdocsDoxyTemplate

def generate(env):
    MkdocsServer.generate(env)
    MkdocsBuild.generate(env)
    MkdocsPublish.generate(env)
    MkdocsJsonBuild.generate(env)


    Mkdocs2Pandoc.generate(env)
    MkdocsDoxyTemplate.generate(env)

def exists(env):
    if (MkdocsServer.exists(env) == False): return False
    if (MkdocsBuild.exists(env) == False): return False
    if (MkdocsPublish.exists(env) == False): return False
    if (MkdocsJsonBuild.exists(env) == False): return False


    if (Mkdocs2Pandoc.exists(env) == False): return False
    if (MkdocsDoxyTemplate.exists(env) == False): return False
    return True
