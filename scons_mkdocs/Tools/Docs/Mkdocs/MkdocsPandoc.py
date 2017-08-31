"""
MkdocsPandoc
  This tool uses mkdocs2pandoc to generate a pd pandoc file which can then be used with pandoc to generate a pdf or other forms of documentation
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
    env.SetDefault(Mkdocs_WorkingDir = env.Dir('.').abspath)
    # Available Options - These override those within the yaml configuration file

    # Set encoding for input files (default: utf-8)
    env.SetDefault(Mkdocs_Pandoc_Encoding = None)
    # Extension to substitute image extensions by (default: no replacement)
    env.SetDefault(Mkdocs_Pandoc_ImageExt = None)
    # Width of generated grid tables in characters (default: 100)
    env.SetDefault(Mkdocs_Pandoc_Width = None)
    # Include files to skip (default: none)
    env.SetDefault(Mkdocs_Pandoc_Exclude = None)
    # Additional Arguments
    env.SetDefault(Mkdocs_ExtraArgs = [])

    # Register the builder
    bld = Builder(action = __MkdocsPandoc_func)
    env.Append(BUILDERS = {'__MkdocsPandoc' : bld})
    env.AddMethod(MkdocsPandoc, 'MkdocsPandoc')


def MkdocsPandoc(env, target = None, source = None):
    """Wrapper for the Builder so that we can use a default on the source parameter"""
    if not source:
        source = File('mkdocs.yml')
    if not target:
        target = File('test1.pd')
        #target = File('site/mkdocs.pd')
    return env.__MkdocsPandoc(target, source)

def __MkdocsPandoc_func(target, source, env):
    """Actual builder that does the work after the Sconscript file is parsed"""

    # TODO VStudio related error while finding this on the path (Scripts) of the virtual env
    cmdopts = ['mkdocs2pandoc']

    index = 0
    for srcitem in source:
        cfgfile = srcitem.abspath
        outfile = target[index].abspath

        if cfgfile:
            cmdopts.append('--config-file=' + cfgfile)

        if outfile:
            cmdopts.append('--outfile=' + outfile)

        if env['Mkdocs_Pandoc_Encoding']:
            cmdopts.append('--encoding=' +  env['Mkdocs_Pandoc_Encoding'])

        if env['Mkdocs_Pandoc_ImageExt']:
            cmdopts.append('--image-ext=' +  env['Mkdocs_Pandoc_ImageExt'])

        if env['Mkdocs_Pandoc_Width']:
            cmdopts.append('--width=' +  env['Mkdocs_Pandoc_Width'])

        # TODO parse list as input
        if env['Mkdocs_Pandoc_Exclude']:
            cmdopts.append('--exclude=' +  env['Mkdocs_Pandoc_Exclude'])

        cmdopts = cmdopts + env['Mkdocs_ExtraArgs']

        print('Building MkDocs Documentation:')
        env.Execute(env.Action([cmdopts], chdir=env['Mkdocs_WorkingDir']))
        index = index + 1
