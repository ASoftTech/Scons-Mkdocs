"""
MkdocsPublish
  This tool will publish the mkdocs content to a github pages destination
"""

# If you ever want to remove the remote published branch you can use something like
# git push origin --delete gh-pages

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
    # If to Remove old files from the site_dir before building (the default).
    env.SetDefault(Mkdocs_CleanBuild = None)
    # If to override the default remote branch setting when uploading
    env.SetDefault(Mkdocs_RemoteBranch = None)
    # If to override the default remote name setting when uploading
    env.SetDefault(Mkdocs_RemoteName = None)
    # If to force the push to github
    env.SetDefault(Mkdocs_ForcePush = False)
    # If to silence warnings
    env.SetDefault(Mkdocs_Quiet = False)
    # Show verbose messages
    env.SetDefault(Mkdocs_Verbose = False)
    # Additional Arguments
    env.SetDefault(Mkdocs_ExtraArgs = [])

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
    cmdopts = ['mkdocs', 'gh-deploy']

    for srcitem in source:
        cfgfile = srcitem.abspath

        if cfgfile:
            cmdopts.append('--config-file=' + cfgfile)

        if env['Mkdocs_CleanBuild'] == True:
            cmdopts.append('--clean')
        elif env['Mkdocs_CleanBuild'] == False:
            cmdopts.append('--dirty')

        if not env['Mkdocs_CommitMsg']:
            raise Exception('No commit message specified')
        cmdopts.append('--message=' + env['Mkdocs_CommitMsg'])

        if env['Mkdocs_RemoteBranch']:
            cmdopts.append('--remote-branch=' + env['Mkdocs_RemoteBranch'])

        if env['Mkdocs_RemoteName']:
            cmdopts.append('--remote-name=' + env['Mkdocs_RemoteName'])
            
        if env['Mkdocs_ForcePush']:
            cmdopts.append('--force')

        if env['Mkdocs_Quiet']:
            cmdopts.append('--quiet')

        if env['Mkdocs_Verbose']:
            cmdopts.append('--verbose')

        cmdopts = cmdopts + env['Mkdocs_ExtraArgs']

        print('Pushing MkDocs Documentation:')
        env.Execute(env.Action([cmdopts], chdir=env['Mkdocs_WorkingDir']))

