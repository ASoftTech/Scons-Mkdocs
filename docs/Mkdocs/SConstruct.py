#!/usr/bin/env python2

# These import lines are not really needed, but it helps intellisense within VS when editing the script
import SCons.Script
from SCons.Environment import Environment

import sys, os

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
    #env.Replace(Mkdocs_ExtraArgs = ['--verbose'])

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
        tgt = env.MkdocsBuilder()
        Default(tgt)
        SetOption('clean', True)



    elif cmd == 'publish':
        print ("TODO publish")


    elif cmd == 'json':
        print ("TODO json")

    elif cmd == 'pdf':
        print ("TODO pdf")

    elif cmd == 'doxygen_templates':
        print ("TODO doxygen_templates")

    else:
        print_useage(env)
        Exit(1)


main()

# Ignore the command line and just use default targets
SCons.Script.BUILD_TARGETS = DEFAULT_TARGETS
