"""
MkdocsServer
This tool can be used to serve / preview the mkdocs output locally before publishing
"""

import os, sys, os.path as path
import SCons.Script
from SCons.Environment import Environment

def exists(env):
    """return True if this tool is valid in this environment"""
    return True

def generate(env):
    """Called when the tool is loaded into the environment at startup of script"""
    assert(exists(env))
    env.SetDefault(Mkdocs_WorkingDir = env.Dir('.').abspath)
    # Available Options - These override those within the yaml configuration file
    # Default is '127.0.0.1:8000'
    env.SetDefault(Mkdocs_ServeUrl = None)
    # If to enable Strict mode
    env.SetDefault(Mkdocs_Strict = False)
    # Which theme to use
    env.SetDefault(Mkdocs_Theme = None)
    # Directory of additional files to merge in with the theme
    env.SetDefault(Mkdocs_ThemeDir = None)
    # If to use livereload, enabled by default
    # when pages change on the file system the browser auto refreshes to show the changes
    env.SetDefault(Mkdocs_LiveReload = None)
    # Enable the live reloading in the development server
    # but only re-build files that have changed
    env.SetDefault(Mkdocs_DirtyReload = False)
    # If to silence warnings
    env.SetDefault(Mkdocs_Quiet = False)
    # Show verbose messages
    env.SetDefault(Mkdocs_Verbose = False)
    # Additional Arguments
    env.SetDefault(Mkdocs_ExtraArgs = [])

    # Register the method
    env.AddMethod(MkdocsServer, 'MkdocsServer')

def MkdocsServer(env, cfgfile = None):
    cmdopts = ['mkdocs', 'serve']

    if cfgfile:
        cmdopts.append('--config-file=' + cfgfile)

    serverurl = '127.0.0.1:8000'
    if env['Mkdocs_ServeUrl']:
        cmdopts.append('--dev-addr=' + env['Mkdocs_ServeUrl'])
        serverurl = env['Mkdocs_ServeUrl']

    if env['Mkdocs_Strict']:
        cmdopts.append('--strict')

    if env['Mkdocs_Theme']:
        cmdopts.append('--theme=' + env['Mkdocs_Theme'])

    if env['Mkdocs_ThemeDir']:
        cmdopts.append('--theme-dir=' + env['Mkdocs_ThemeDir'])

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
