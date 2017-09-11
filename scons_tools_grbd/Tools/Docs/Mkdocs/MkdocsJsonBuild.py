"""
MkdocsJsonBuild
  This tool will generate the documentation output as json using markdown files as an input
  via mkdocs to an output directory
"""

import os, sys, os.path as path
import SCons.Script
from SCons.Environment import Environment
from SCons.Script import Builder

# TODO fix relative imports when importing a single namespaced tool
from scons_tools_grbd.Tools.Docs.Mkdocs import MkdocsCommon


def exists(env):
    """Check if we're okay to load this builder"""
    return MkdocsCommon.detect(env)


def generate(env):
    """Called when the tool is loaded into the environment at startup of script"""
    assert(exists(env))
    MkdocsCommon.setup_opts(env)
    mkdocs_scanner = env.Scanner(
        MkdocsCommon.MkdocsScanner,
        'MkdocsScanner',
    )
    bld = Builder(
        action = __MkdocsJsonBuild_func,
        emitter = MkdocsCommon.Mkdocs_emitter,
        source_scanner = mkdocs_scanner,
    )
    env.Append(BUILDERS = {'MkdocsJsonBuild' : bld})


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
