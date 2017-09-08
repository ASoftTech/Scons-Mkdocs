"""
DoxygenCommon
  Common code associated with doxygen builders
"""

import os, sys, os.path as path, yaml
import SCons.Script
from SCons.Environment import Environment
from SCons.Script import File, Dir

def detect(env):
    """Detect if mkdocs exe is detected on the system, or use user specified option"""
    if 'Mkdocs' in env:
        return env.Detect(env['Doxygen'])
    else:
        return env.Detect('doxygen')

def setup_opts(env):
    """Common setup of options for Mkdocs builders"""
    # Available Options - These override those within the yaml configuration file
    env.SetDefault(
        # Default exe to launch
        Doxygen = 'doxygen',
        # Working directory is current directory (default)
        Doxygen_WorkingDir = env.Dir('.'),

        # Additional Arguments
        Doxygen_ExtraArgs = [],
        )

def Doxygen_emitter(target, source, env):
    # Choose mkdocs.yml as source file if not specified
    if not source:
        cfgfile = File('Doxyfile')
        source.append(cfgfile)
    else:
        cfgfile = source[0]
    
    # TODO
    # Read mkdocs config
    #yamlcfg, sitedirnode, docsdirnode = Mkdocs_Readconfig(cfgfile, env)
    # Add in the contents of the docs source directory
    #source = source + MkdocsScanner(docsdirnode, env, None, None)
    # We need at least one target that's a file for the rebuild if source changes logic to work
    #filenode = File(path.join(str(sitedirnode), 'mkdocs/search_index.json'))
    #target.append(filenode)
    #env.Clean(target, sitedirnode)
    return target, source
