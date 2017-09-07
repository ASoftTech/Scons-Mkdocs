"""
MkdocsBuild
  This tool will generate the documentation output as html using markdown files as an input
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
    bld = Builder(action = __MkdocsBuild_func, emitter = MkdocsCommon.Mkdocs_emitter)
    env.Append(BUILDERS = {'MkdocsBuild' : bld})


def __MkdocsBuild_func(target, source, env):
    """Actual builder that does the work after the Sconscript file is parsed"""
    cmdopts = ['$Mkdocs', 'build']
    cmdopts.append('--config-file=' + str(source[0]))
    if env['Mkdocs_CleanBuild'] == True:
        cmdopts.append('--clean')
    elif env['Mkdocs_CleanBuild'] == False:
        cmdopts.append('--dirty')
    if env['Mkdocs_Strict']:
        cmdopts.append('--strict')
    if env['Mkdocs_Theme']:
        cmdopts.append('--theme=$Mkdocs_Theme')
    if env['Mkdocs_ThemeDir']:
        cmdopts.append('--theme-dir=$Mkdocs_ThemeDir')
    if env['Mkdocs_SiteDir']:
        cmdopts.append('--site-dir=$Mkdocs_SiteDir')
    if env['Mkdocs_Quiet']:
        cmdopts.append('--quiet')
    if env['Mkdocs_Verbose']:
        cmdopts.append('--verbose')
    cmdopts = cmdopts + env['Mkdocs_ExtraArgs']

    print('Building MkDocs Documentation:')
    env.Execute(env.Action([cmdopts], chdir=env['Mkdocs_WorkingDir']))
