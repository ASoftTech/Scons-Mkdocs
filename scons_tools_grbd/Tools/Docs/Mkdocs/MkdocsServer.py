"""
MkdocsServer
This tool can be used to serve / preview the mkdocs output locally before publishing
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
    bld = Builder(action = __MkdocsServer_func, emitter = __MkdocsServerBuild_emitter)
    env.Append(BUILDERS = {'MkdocsServer' : bld})


def __MkdocsServerBuild_emitter(target, source, env):
    # TODO read / parse mkdocs.yml
    # change in source not triggering rebuild?

    # Choose mkdocs.yml as source file if not specified
    if not source:
        source.append(File('mkdocs.yml'))
    # Add in the contents of the docs directory
    source = source + MkdocsCommon.MkdocsScanner(Dir('docs'), env)
    return target, source


def __MkdocsServer_func(target, source, env):
    """Actual builder that does the work after the Sconscript file is parsed"""
    cmdopts = ['$Mkdocs', 'serve']
    cmdopts.append('--config-file=' + str(source[0]))
    serverurl = '127.0.0.1:8000'
    if env['Mkdocs_ServeUrl']:
        serverurl = str(env['Mkdocs_ServeUrl'])
        cmdopts.append('--dev-addr=$Mkdocs_ServeUrl')
    if env['Mkdocs_Strict']:
        cmdopts.append('--strict')
    if env['Mkdocs_Theme']:
        cmdopts.append('--theme=$Mkdocs_Theme')
    if env['Mkdocs_ThemeDir']:
        cmdopts.append('--theme-dir=$Mkdocs_ThemeDir')
    if env['Mkdocs_LiveReload'] == True:
        cmdopts.append('--livereload')
    elif env['Mkdocs_LiveReload'] == False:
        cmdopts.append('--no-livereload')
    if env['Mkdocs_DirtyReload'] == True:
        cmdopts.append('--dirtyreload')
    if env['Mkdocs_Quiet']:
        cmdopts.append('--quiet')
    if env['Mkdocs_Verbose']:
        cmdopts.append('--verbose')
    cmdopts = cmdopts + env['Mkdocs_ExtraArgs']

    print('Starting MkDocs Server http://' + serverurl)
    env.Execute(env.Action([cmdopts], chdir=env['Mkdocs_WorkingDir']))
    print ("Server Closed.")
