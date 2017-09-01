"""
MkdocsBuild
  This tool will generate the documentation output as html using markdown files as an input
  via mkdocs to an output directory
"""

import os, sys, os.path as path
import SCons.Script
from SCons.Environment import Environment
from SCons.Script import *

def exists(env):
    """Make sure mkdocs exists"""
    return env.Detect("mkdocs")

def generate(env):
    """Called when the tool is loaded into the environment at startup of script"""
    assert(exists(env))
    env.SetDefault(Mkdocs_WorkingDir = env.Dir('.').abspath)
    # Available Options - These override those within the yaml configuration file
    # If to Remove old files from the site_dir before building (the default).
    env.SetDefault(Mkdocs_CleanBuild = None)
    # If to enable Strict mode
    env.SetDefault(Mkdocs_Strict = False)
    # Which theme to use
    env.SetDefault(Mkdocs_Theme = None)
    # Directory of additional files to merge in with the theme
    env.SetDefault(Mkdocs_ThemeDir = None)
    # Directory to output the build to - default is 'site'
    env.SetDefault(Mkdocs_SiteDir = None)
    # If to silence warnings
    env.SetDefault(Mkdocs_Quiet = False)
    # Show verbose messages
    env.SetDefault(Mkdocs_Verbose = False)
    # Additional Arguments
    env.SetDefault(Mkdocs_ExtraArgs = [])

    # Register the builder
    bld = Builder(action = __MkdocsBuild_func, emitter = __MkdocsBuild_modify_targets)
    env.Append(BUILDERS = {'__MkdocsBuild' : bld})
    env.AddMethod(MkdocsBuild, 'MkdocsBuild')


def MkdocsBuild(env, source = None):
    """Wrapper for the Builder so that we can use a default on the source parameter"""
    if source:
        return env.__MkdocsBuild(source)
    else:
        return env.__MkdocsBuild('mkdocs.yml')


def __MkdocsBuild_modify_targets(target, source, env):
    del target[:]
    if env['Mkdocs_SiteDir']:
        dirnode = Dir(env['Mkdocs_SiteDir'])
    else:
        dirnode = Dir('site')
    target.append(dirnode)

    env.Clean(target, dirnode)
    return target, source


def __MkdocsBuild_func(target, source, env):
    """Actual builder that does the work after the Sconscript file is parsed"""
    cmdopts = ['mkdocs', 'build']

    for srcitem in source:
        cfgfile = str(srcitem)

        if cfgfile:
            cmdopts.append('--config-file=' + cfgfile)

        if env['Mkdocs_CleanBuild'] == True:
            cmdopts.append('--clean')
        elif env['Mkdocs_CleanBuild'] == False:
            cmdopts.append('--dirty')

        if env['Mkdocs_Strict']:
            cmdopts.append('--strict')

        if env['Mkdocs_Theme']:
            cmdopts.append('--theme=' + str(env['Mkdocs_Theme']))

        if env['Mkdocs_ThemeDir']:
            cmdopts.append('--theme-dir=' + str(env['Mkdocs_ThemeDir']))

        if env['Mkdocs_SiteDir']:
            cmdopts.append('--site-dir=' + str(env['Mkdocs_SiteDir']))

        if env['Mkdocs_Quiet']:
            cmdopts.append('--quiet')

        if env['Mkdocs_Verbose']:
            cmdopts.append('--verbose')

        cmdopts = cmdopts + env['Mkdocs_ExtraArgs']

        print('Building MkDocs Documentation:')
        env.Execute(env.Action([cmdopts], chdir=env['Mkdocs_WorkingDir']))
