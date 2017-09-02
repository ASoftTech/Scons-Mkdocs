"""
Mkdocs2Pandoc
  This tool uses mkdocs2pandoc to generate a pd pandoc file which can then be used with pandoc to generate a pdf or other forms of documentation
"""

import os, sys, os.path as path
import SCons.Script
from SCons.Environment import Environment
from SCons.Script import *


def _detect(env):
    if 'Mkdocs2pandoc' in env:
        return env['Mkdocs2pandoc']
    return env.Detect("mkdocs2pandoc")

def exists(env):
    return _detect(env)


def generate(env):
    """Called when the tool is loaded into the environment at startup of script"""
    assert(exists(env))
    # Available Options - These override those within the yaml configuration file
    env.SetDefault(
        # Working directory is current directory (default)
        Mkdocs_WorkingDir = env.Dir('.'),
        # Set encoding for input files (default: utf-8)
        Mkdocs_Pandoc_Encoding = None,
        # Extension to substitute image extensions by (default: no replacement)
        Mkdocs_Pandoc_ImageExt = None,
        # Width of generated grid tables in characters (default: 100)
        Mkdocs_Pandoc_Width = None,
        # Include files to skip (default: none)
        Mkdocs_Pandoc_Exclude = None,
        # Additional Arguments
        Mkdocs_ExtraArgs = [],
        )

    # Register the builder
    bld = Builder(action = __Mkdocs2Pandoc_func)
    env.Append(BUILDERS = {'__Mkdocs2Pandoc' : bld})
    env.AddMethod(Mkdocs2Pandoc, 'Mkdocs2Pandoc')


def Mkdocs2Pandoc(env, target = None, source = None):
    """Wrapper for the Builder so that we can use a default on the source parameter"""
    if not source:
        source = File('mkdocs.yml')
    if not target:
        target = File('docs/site.pd')
    return env.__Mkdocs2Pandoc(target, source)


def __Mkdocs2Pandoc_func(target, source, env):
    """Actual builder that does the work after the Sconscript file is parsed"""
    cmdopts = [_detect(env)]

    index = 0
    for srcitem in source:
        cfgfile = str(srcitem)
        outfile = str(target[index])

        if cfgfile:
            cmdopts.append('--config-file=' + cfgfile)

        if outfile:
            cmdopts.append('--outfile=' + outfile)

        if env['Mkdocs_Pandoc_Encoding']:
            cmdopts.append('--encoding=' + str(env['Mkdocs_Pandoc_Encoding']))

        if env['Mkdocs_Pandoc_ImageExt']:
            cmdopts.append('--image-ext=' + str(env['Mkdocs_Pandoc_ImageExt']))

        if env['Mkdocs_Pandoc_Width']:
            cmdopts.append('--width=' + str(env['Mkdocs_Pandoc_Width']))

        # TODO parse list as input
        if env['Mkdocs_Pandoc_Exclude']:
            cmdopts.append('--exclude=' + str(env['Mkdocs_Pandoc_Exclude']))

        cmdopts = cmdopts + env['Mkdocs_ExtraArgs']

        print('Building MkDocs Documentation as Pandoc file:')
        env.Execute(env.Action([cmdopts], chdir=env['Mkdocs_WorkingDir']))
        index = index + 1
