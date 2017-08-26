#!/usr/bin/env python2

# These import lines are not really needed, but it helps intellisense within VS when editing the script
import SCons.Script
from SCons.Environment import Environment

import sys, os

# TODO pass additional command line args to the process via an additional args setting

# TODO remove once we can install via pip
oldsyspath = sys.path
dir_path = Dir('.').srcnode().abspath
dir_path = os.path.join(dir_path, '../../')
dir_path = os.path.abspath(dir_path)
sys.path.append(dir_path)


def print_useage(env):
    print ("Please use scons <target> where <target> is one of")
    print ("  build         to make standalone HTML files")
    print ("  build_doxygen to build Doxygen related files")
    print ("  clean         to clean the output directory: " + env['Mkdocs_BuildDir'])
    print ("  publish       publish the site to the gh-pages branch")
    print ("  serve         Serve the site out on a port for demoing")


def setup_opts(env):
    """Optionally change the default options"""
    #env.Replace(Mkdocs_WorkingDir = env.Dir('.').abspath)
    #env.Replace(Mkdocs_ServeUrl = '127.0.0.1:8001')
    #env.Replace(Mkdocs_Strict = 'True')
    env.Replace(Mkdocs_Theme = 'cyborg')
    #env.Replace(Mkdocs_ThemeDir = 'theme')
    #env.Replace(Mkdocs_DirtyReload = True)
    #env.Replace(Mkdocs_SiteDir = 'site2')

    env.Replace(Mkdocs_ExtraArgs = ['--verbose'])

    # Location of the Markdown / Site Source
    #env.Replace(Mkdocs_SrcDir = os.path.join(scriptdir, 'docs'))
    # Destination for the Build of the site
    #env.Replace(Mkdocs_BuildDir = os.path.join(scriptdir, 'site'))
    # TODO DOXYDIR
    # TODO DOXYBUILDDIR

    # Check version of scons
    EnsureSConsVersion(3,0,0)


def main():
    # Setup environment
    env = Environment(ENV = os.environ, tools = ['Docs.Mkdocs'], toolpath = [PyPackageDir('scons_mkdocs.Tools')])
    setup_opts(env)

    # Use the first parameter as the mode to run as
    if len(COMMAND_LINE_TARGETS) > 0:
        cmd = COMMAND_LINE_TARGETS[0]
    else:
        print_useage(env)
        Exit(1)

    if cmd == 'serve':
        env.MkdocsServer()
        Exit(0)

    elif cmd == 'build':
        #tgt = env.MkdocsBuilder('mkdocs.yml')
        tgt = env.MkdocsBuilder()
        Default(tgt)

    elif cmd == 'clean':
        print ("TODO clean")

    elif cmd == 'build_doxygen':
        print ("TODO build_doxygen")

    elif cmd == 'publish':
        print ("TODO publish")

    else:
        print_useage(env)
        Exit(1)


main()

# Ignore the command line and just use default targets
SCons.Script.BUILD_TARGETS = DEFAULT_TARGETS






# After this point any builders we've setup will run / generate the docs

# TODO remove this if we use builders
#Exit(0)

# Environment variables
# 1. Mkdocs_SourceDir
# 2. Mkdocs_BuildDir
# 3. Mkdocs_RootDir

# Doxygen template variables
# we need the root of the doxygen dir
# And the html template dir used by doxygen

# 1. Builder / Clean
# 2. Publisher
# 3. Generate Doxygen templates














#import os, sys
#import os.path as path
#import opts.opts_common
#import opts.opts_dotnet

# Setup environment
#env = Environment(ENV = os.environ)

# Check version of scons
#EnsureSConsVersion(2,5,1)

#sys.path.append("D:\\SourceControl\\GitRepos\\scons-contrib\\sconscontrib\\SCons\\Tool")


#from MSBuild.dll2lib import Dll2Lib

#x1 = Dll2Lib()



#path1 = path.abspath('D:\\SourceControl\\GitRepos\\scons-contrib\\sconscontrib\\SCons\\Tool')

# Test sconscontrib / toolpath

# Test python module
#env = Environment(ENV = os.environ, tools = ['testtool1'], toolpath = [path1])
# Test python package
#env = Environment(ENV = os.environ, tools = ['testtool2'], toolpath = [path1])
# Test python package nested 1 level
#env = Environment(ENV = os.environ, tools = ['MSBuild.testtool3'], toolpath = [path1])
# Test python package nested 2 level
#env = Environment(ENV = os.environ, tools = ['MSBuild.test1.testtool4'], toolpath = [path1])


# Test scons local tools

#env = Environment(ENV = os.environ, tools = ['testtool1'])
#env = Environment(ENV = os.environ, tools = ['testtool2'])
#env = Environment(ENV = os.environ, tools = ['MSBuild.testtool3'])
#env = Environment(ENV = os.environ, tools = ['MSBuild.test1.testtool4'])

#env.Dll2Lib('C:\\Program Files\\GTK3-Runtime Win64\\bin')

# todo
# 1. run sys tests for win / linux / py2 / py3 / patched / unpatched
#    run a diff between the tests, look for leaky handles in the diff


## Setup options
#opts.opts_common.setup_opts(env)

## Setup variables
#vars = Variables(path.join(env['common_builddir'], 'config.py'), ARGUMENTS)
#vars = opts.opts_common.setup_vars(env, vars)
#vars = opts.opts_dotnet.setup_vars(env, vars)
#Help(vars.GenerateHelpText(env))

#Export('env')

## Build C# Libs
#SConscript('Source/Libs/SConscript.py')

# Build Glue Libs
#SConscript('Source/Libs-Glue/SConscript.py')

# Check if we need to save the build variables
#opts.opts_common.check_save(env, vars)
