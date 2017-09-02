"""
MkdocsBuild
  This tool will generate the documentation output as html using markdown files as an input
  via mkdocs to an output directory
"""

import os, sys, os.path as path
import SCons.Script
from SCons.Environment import Environment
from SCons.Script import *

def _detect(env):
    if 'Mkdocs' in env:
        return env['Mkdocs']
    return env.Detect("mkdocs")

def exists(env):
    return _detect(env)

def generate(env):
    """Called when the tool is loaded into the environment at startup of script"""
    assert(exists(env))
    # Available Options - These override those within the yaml configuration file
    env.SetDefault(
        # Working directory is current directory (default)
        Mkdocs_WorkingDir = env.Dir('.'),
        # If to Remove old files from the site_dir before building (the default).
        Mkdocs_CleanBuild = None,
        # If to enable Strict mode
        Mkdocs_Strict = False,
        # Which theme to use
        Mkdocs_Theme = None,
        # Directory of additional files to merge in with the theme
        Mkdocs_ThemeDir = None,
        # Directory to output the build to - default is 'site'
        Mkdocs_SiteDir = None,
        # If to silence warnings
        Mkdocs_Quiet = False,
        # Show verbose messages
        Mkdocs_Verbose = False,
        # Additional Arguments
        Mkdocs_ExtraArgs = [],
        )

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
    cmdopts = [_detect(env), 'build']

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
