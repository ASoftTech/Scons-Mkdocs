"""
MkdocsPublish
  This tool will publish the mkdocs content to a github pages destination
"""

# If you ever want to remove the remote published branch you can use something like
# git push origin --delete gh-pages

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
        action = __MkdocsPublish_func,
        emitter = MkdocsCommon.Mkdocs_emitter,
        source_scanner = mkdocs_scanner,
    )
    env.Append(BUILDERS = {'__MkdocsPublish' : bld})
    env.AddMethod(MkdocsPublish, 'MkdocsPublish')


def MkdocsPublish(env, commitmsg, target = None, source = None):
    """Wrapper for the Builder so that we can use a default on the source parameter"""
    return env.__MkdocsPublish(target, source, Mkdocs_CommitMsg=commitmsg)


def __MkdocsPublish_func(target, source, env):
    """Actual builder that does the work after the Sconscript file is parsed"""
    cmdopts = ['$Mkdocs', 'gh-deploy']
    cmdopts.append('--config-file=' + str(source[0]))
    if env['Mkdocs_CleanBuild'] == True:
        cmdopts.append('--clean')
    elif env['Mkdocs_CleanBuild'] == False:
        cmdopts.append('--dirty')
    if not env['Mkdocs_CommitMsg']:
        raise Exception('No commit message specified')
    cmdopts.append('--message="$Mkdocs_CommitMsg"')
    if env['Mkdocs_RemoteBranch']:
        cmdopts.append('--remote-branch=$Mkdocs_RemoteBranch')
    if env['Mkdocs_RemoteName']:
        cmdopts.append('--remote-name=$Mkdocs_RemoteName')
    if env['Mkdocs_ForcePush']:
        cmdopts.append('--force')
    if env['Mkdocs_Quiet']:
        cmdopts.append('--quiet')
    if env['Mkdocs_Verbose']:
        cmdopts.append('--verbose')
    cmdopts = cmdopts + env['Mkdocs_ExtraArgs']

    print('Pushing MkDocs Documentation:')
    env.Execute(env.Action([cmdopts], chdir=env['Mkdocs_WorkingDir']))
