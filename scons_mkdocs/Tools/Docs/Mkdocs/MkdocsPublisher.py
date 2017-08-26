"""
MkdocsPublisher
  This tool will publish the mkdocs content to a github pages destination
"""

import os, sys
import os.path as path
from SCons.Script import *

def exists(env):
    """return True if this tool is valid in this environment"""
    return True

def generate(env):
    """Called when the tool is loaded into the environment at startup of script"""
    assert(exists(env))
    # TODO

