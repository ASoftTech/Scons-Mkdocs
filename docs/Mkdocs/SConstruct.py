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

def main():
    # Setup environment
    EnsureSConsVersion(3,0,0)
    env = Environment(ENV = os.environ, tools = ['default', 'Docs.Mkdocs', 'MSBuild'], toolpath = [PyPackageDir('scons_tools_grbd.Tools')])
    setup_opts(env)

    # Use the first parameter as the mode to run as
    if len(COMMAND_LINE_TARGETS) > 0:
        cmd = COMMAND_LINE_TARGETS[0]
    else:
        print_useage(env)
        Exit(1)

    if cmd == 'serve':
        tgt = env.MkdocsServer()
        Default(tgt)

    elif cmd == 'build':
        manual_clean(env)
        tgt = env.MkdocsBuild()
        Default(tgt)

    elif cmd == 'publish':
        manual_clean(env)
        tgt = env.MkdocsPublish("Example commit message")
        Default(tgt)

    elif cmd == 'clean':
        clean(env)

    # Alternative Formats

    elif cmd == 'json':
        manual_clean(env)
        tgt = env.MkdocsJsonBuild()
        Default(tgt)

    elif cmd == 'mkcombine':
        manual_clean(env)
        tgt = env.MkdocsCombiner()
        Default(tgt)





    # TODO


    elif cmd == 'pdf':
        manual_clean(env)
        markdown_target = env.MkdocsCombiner()
        pd_target = env.Pandoc('docs/export/site.pdf', markdown_target)
        Default(pd_target)


    elif cmd == 'doxygen':
        print ("TODO doxygen_templates")

    else:
        print_useage(env)
        Exit(1)


def print_useage(env):
    print ("Please use scons <target> where <target> is one of")
    print ("  serve         Serve the site out on a port for demoing")
    print ("  build         to build the documentation as HTML files")
    print ("  publish       publish the site to the gh-pages branch")
    print ("  clean         to clean the output directory")

    print ("Alternative Formats:")
    print ("  json          to build the documentation as JSON files")
    print ("  mkcombine     to build the documentation as a combined markdown file")

    # TODO
    print ("  pdf           to build the documentation as a pdf")
    print ("  doxygen       to build Doxygen related files to be inserted into the docs")




# Clean using the SCons build system
def clean(env):
    tgt = env.MkdocsBuild()
    Default(tgt)
    SetOption('clean', True)


## Manual Clean of Build directory without using scons
## This is due to scons not yet supporting a clean and build at the same time.
def manual_clean(env):
    print("Cleaning Output dir")
    sitedir = env['Mkdocs_SiteDir']
    if not sitedir:
        sitedir = 'site'
    sitedir = os.path.abspath(sitedir)
    Execute(Delete(sitedir))


def setup_opts(env):
    """Optionally change the default options"""
    env.Replace(Mkdocs_Theme = 'cyborg')
    env.Replace(Mkdocs_CleanBuild = True)

    env.Replace(Mkdocs = 'mkdocs')

    #env.Replace(Mkdocs_WorkingDir = env.Dir('.'))
    #env.Replace(Mkdocs_ServeUrl = '127.0.0.1:8001')
    #env.Replace(Mkdocs_Strict = True)
    #env.Replace(Mkdocs_ThemeDir = Dir('theme'))
    #env.Replace(Mkdocs_DirtyReload = True)
    #env.Replace(Mkdocs_SiteDir = 'site2')
    #env.Replace(Mkdocs_ExtraArgs = ['--verbose'])

    # Location of the Markdown / Site Source
    #env.Replace(Mkdocs_SrcDir = os.path.join(scriptdir, 'docs'))
    # Destination for the Build of the site
    #env.Replace(Mkdocs_BuildDir = os.path.join(scriptdir, 'site'))
    # TODO DOXYDIR
    # TODO DOXYBUILDDIR


main()

# Ignore the command line and just use default targets
SCons.Script.BUILD_TARGETS = DEFAULT_TARGETS
