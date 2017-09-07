"""
DotnetCoreBuild
  This tool run the 'dotnet' tool in 'build' mode for use with .Net Core
"""

# See https://docs.microsoft.com/en-us/dotnet/core/tools/dotnet-build?tabs=netcore2x

# TODO add scanner

import os, sys, os.path as path
import SCons.Script
from SCons.Environment import Environment
from SCons.Script import *

def _detect(env):
    if 'DOTNETCORE' in env:
        return env['DOTNETCORE']
    return env.Detect("dotnet")

def exists(env):
    return _detect(env)

def generate(env):
    """Called when the tool is loaded into the environment at startup of script"""
    assert(exists(env))
    # Available Options - These override those within the yaml configuration file
    env.SetDefault(
        # Working directory is current directory (default)
        DotnetCore_WorkingDir = env.Dir('.'),
        # Defines the build configuration. The default value is Debug
        DotnetCore_Config = None,
        # Compiles for a specific framework. The framework must be defined in the project file.
        DotnetCore_Framework = None,
        # Forces all dependencies to be resolved even if the last restore was successful.
        # This is equivalent to deleting the project.assets.json file.
        DotnetCore_Force = False,
        # Ignores project-to-project (P2P) references and only builds the root project specified to build.
        DotnetCore_IgnoreDepends = False,
        # Marks the build as unsafe for incremental build.
        # This turns off incremental compilation and forces a clean rebuild of the project's dependency graph.
        DotnetCore_DisableIncremental = False,
        # If True Doesn't perform an implicit restore during build.
        DotnetCore_NoRestore = False,
        # Directory in which to place the built binaries. You also need to define --framework when you specify this option.
        DotnetCore_OutputDir = None,
        # Specifies the target runtime. For a list of Runtime Identifiers (RIDs), see the RID catalog.
        DotnetCore_Runtime = None,
        # Sets the verbosity level of the command. Allowed values are q[uiet], m[inimal], n[ormal], d[etailed], and diag[nostic]
        DotnetCore_Verbosity = None,
        # Defines the version suffix for an asterisk (*) in the version field of the project file.
        # The format follows NuGet's version guidelines.
        DotnetCore_VersionSuffix = None,
        # Additional Arguments
        DotnetCore_ExtraArgs = [],
        )

    # Register the builder
    bld = Builder(action = __DotnetCoreBuild_func, emitter = __DotnetCoreBuild_modify_targets)
    env.Append(BUILDERS = {'DotnetCoreBuild' : bld})


def __DotnetCoreBuild_modify_targets(target, source, env):
    # TODO
    return target, source


def __MkdocsBuild_func(target, source, env):
    """Actual builder that does the work after the Sconscript file is parsed"""
    cmdopts = [_detect(env), 'build']

    for srcitem in source:
        srcfile = str(srcitem)

        if srcfile:
            cmdopts.append(srcfile)

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
