"""
DotnetCoreBuild
  This tool run the 'dotnet' tool in 'build' mode for use with .Net Core
"""

# See https://docs.microsoft.com/en-us/dotnet/core/tools/dotnet-build?tabs=netcore2x

# TODO add scanner

import os, sys, os.path as path
import SCons.Script
from SCons.Environment import Environment
from SCons.Script import Builder

# TODO fix relative imports when importing a single namespaced tool
from scons_tools_grbd.Tools.MSBuild.DotNetCore import DotnetCoreCommon


def exists(env):
    """Check if we're okay to load this builder"""
    return DotnetCoreCommon.detect(env)


def generate(env):
    """Called when the tool is loaded into the environment at startup of script"""
    assert(exists(env))
    DotnetCoreCommon.setup_opts(env)
    bld = Builder(action = __DotnetCoreBuild_func, emitter = __DotnetCoreBuild_emitter)
    env.Append(BUILDERS = {'DotnetCoreBuild' : bld})


def __DotnetCoreBuild_emitter(target, source, env):
    # TODO
    return target, source


def __DotnetCoreBuild_func(target, source, env):
    """Actual builder that does the work after the Sconscript file is parsed"""
    cmdopts = ['$DotnetCore', 'build']

    for srcitem in source:
        cmdopts.append(str(srcitem))
        if env['DotnetCore_Config']:
            cmdopts.append('--configuration $DotnetCore_Config')
        if env['DotnetCore_Framework']:
            cmdopts.append('--framework $DotnetCore_Framework')
        if env['DotnetCore_Force']:
            cmdopts.append('--force')
        if env['DotnetCore_IgnoreDepends']:
            cmdopts.append('--no-dependencies')
        if env['DotnetCore_DisableIncremental']:
            cmdopts.append('--no-incremental')
        if env['DotnetCore_NoRestore']:
            cmdopts.append('--no-restore')
        if env['DotnetCore_OutputDir']:
            cmdopts.append('--output $DotnetCore_OutputDir')
        if env['DotnetCore_Runtime']:
            cmdopts.append('--runtime $DotnetCore_Runtime')
        if env['DotnetCore_Verbosity']:
            cmdopts.append('--verbosity $DotnetCore_Verbosity')
        if env['DotnetCore_VersionSuffix']:
            cmdopts.append('--version-suffix $DotnetCore_VersionSuffix')
        cmdopts = cmdopts + env['DotnetCore_ExtraArgs']

        print('Building dotnet core project:')
        env.Execute(env.Action([cmdopts], chdir=env['DotnetCore_WorkingDir']))
