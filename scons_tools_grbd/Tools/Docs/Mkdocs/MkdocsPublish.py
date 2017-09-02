"""
MkdocsPublish
  This tool will publish the mkdocs content to a github pages destination
"""

# If you ever want to remove the remote published branch you can use something like
# git push origin --delete gh-pages

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
        # If to override the default remote branch setting when uploading
        Mkdocs_RemoteBranch = None,
        # If to override the default remote name setting when uploading
        Mkdocs_RemoteName = None,
        # If to force the push to github
        Mkdocs_ForcePush = False,
        # If to silence warnings
        Mkdocs_Quiet = False,
        # Show verbose messages
        Mkdocs_Verbose = False,
        # Additional Arguments
        Mkdocs_ExtraArgs = [],
        )

    # Register the builder
    bld = Builder(action = __MkdocsPublish_func, emitter = __MkdocsPublish_modify_targets)
    env.Append(BUILDERS = {'__MkdocsPublish' : bld})
    env.AddMethod(MkdocsPublish, 'MkdocsPublish')


def MkdocsPublish(env, commitmsg, source = None):
    """Wrapper for the Builder so that we can use a default on the source parameter"""
    if source:
        return env.__MkdocsPublish(None, source, Mkdocs_CommitMsg=commitmsg)
    else:
        return env.__MkdocsPublish(None, 'mkdocs.yml', Mkdocs_CommitMsg=commitmsg)


def __MkdocsPublish_modify_targets(target, source, env):
    del target[:]
    if env['Mkdocs_SiteDir']:
        dirnode = Dir(env['Mkdocs_SiteDir'])
    else:
        dirnode = Dir('site')
    target.append(dirnode)

    env.Clean(target, dirnode)
    return target, source


def __MkdocsPublish_func(target, source, env):
    """Actual builder that does the work after the Sconscript file is parsed"""
    cmdopts = [_detect(env), 'gh-deploy']

    for srcitem in source:
        cfgfile = str(srcitem)

        if cfgfile:
            cmdopts.append('--config-file=' + cfgfile)

        if env['Mkdocs_CleanBuild'] == True:
            cmdopts.append('--clean')
        elif env['Mkdocs_CleanBuild'] == False:
            cmdopts.append('--dirty')

        if not env['Mkdocs_CommitMsg']:
            raise Exception('No commit message specified')
        cmdopts.append('--message=' + str(env['Mkdocs_CommitMsg']))

        if env['Mkdocs_RemoteBranch']:
            cmdopts.append('--remote-branch=' + str(env['Mkdocs_RemoteBranch']))

        if env['Mkdocs_RemoteName']:
            cmdopts.append('--remote-name=' + str(env['Mkdocs_RemoteName']))
            
        if env['Mkdocs_ForcePush']:
            cmdopts.append('--force')

        if env['Mkdocs_Quiet']:
            cmdopts.append('--quiet')

        if env['Mkdocs_Verbose']:
            cmdopts.append('--verbose')

        cmdopts = cmdopts + env['Mkdocs_ExtraArgs']

        print('Pushing MkDocs Documentation:')
        env.Execute(env.Action([cmdopts], chdir=env['Mkdocs_WorkingDir']))

