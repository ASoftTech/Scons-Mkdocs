"""
MkdocsJsonBuild
  This tool will generate the documentation output as json using markdown files as an input
  via mkdocs to an output directory
"""

import os, sys, os.path as path
import SCons.Script
from SCons.Environment import Environment
from SCons.Script import *

# TODO fix relative imports when importing a single namespaced tool
from scons_tools_grbd.Tools.Docs.Mkdocs import MkdocsCommon


def exists(env):
    """Check if we're okay to load this builder"""
    return MkdocsCommon.detect(env)


def generate(env):
    """Called when the tool is loaded into the environment at startup of script"""
    assert(exists(env))
    MkdocsCommon.setup_opts(env)
    bld = Builder(action = __MkdocsJsonBuild_func, emitter = __MkdocsJsonBuild_emitter)
    env.Append(BUILDERS = {'MkdocsJsonBuild' : bld})


def __MkdocsJsonBuild_emitter(target, source, env):
    # TODO read / parse mkdocs.yml
    # change in source not triggering rebuild?

    # Choose mkdocs.yml as source file if not specified
    if not source:
        source.append(File('mkdocs.yml'))
    # Add in the contents of the docs directory
    source = source + MkdocsCommon.MkdocsScanner(Dir('docs'), env)

    # Change target to site directory
    if env['Mkdocs_SiteDir']:
        dirnode = Dir(env['Mkdocs_SiteDir'])
    else:
        dirnode = Dir('site')
    target.append(dirnode)
    env.Clean(target, dirnode)
    return target, source


def __MkdocsJsonBuild_func(target, source, env):
    """Actual builder that does the work after the Sconscript file is parsed"""
    cmdopts = ['$Mkdocs', 'json']
    cmdopts.append('--config-file=' + str(source[0]))
    if env['Mkdocs_CleanBuild'] == True:
        cmdopts.append('--clean')
    elif env['Mkdocs_CleanBuild'] == False:
        cmdopts.append('--dirty')
    if env['Mkdocs_Strict']:
        cmdopts.append('--strict')
    if env['Mkdocs_SiteDir']:
        cmdopts.append('--site-dir=$Mkdocs_SiteDir')
    if env['Mkdocs_Quiet']:
        cmdopts.append('--quiet')
    if env['Mkdocs_Verbose']:
        cmdopts.append('--verbose')
    cmdopts = cmdopts + env['Mkdocs_ExtraArgs']

    print('Building MkDocs Documentation as Json:')
    env.Execute(env.Action([cmdopts], chdir=env['Mkdocs_WorkingDir']))
