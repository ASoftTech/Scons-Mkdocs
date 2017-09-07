"""
DotnetCoreCommon
  Common code associated with the dotnet core cli tool
"""

import os, sys, os.path as path
import SCons.Script
from SCons.Environment import Environment
from SCons.Script import File, Dir


def detect(env):
    """Detect if dotnet exe is detected on the system, or use user specified option"""
    if 'DotnetCore' in env:
        return env.Detect(env['DotnetCore'])
    else:
        return env.Detect('dotnet')


def setup_opts(env):
    """Common setup of options for dotnet core builders"""
    # Available Options
    env.SetDefault(
        # Default exe to launch
        DotnetCore = 'dotnet',
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
