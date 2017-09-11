# These import lines are not really needed, but it helps intellisense within VS when editing the script
import SCons.Script
from SCons.Environment import Environment

import sys, os

# Set PYTHONPATH before using if running without scons_tools_grbd installed via pip

import SCons.compat
import pickle
SCons.compat.PICKLE_PROTOCOL = pickle.HIGHEST_PROTOCOL



def main():
    # Setup environment
    EnsureSConsVersion(3,0,0)
    env = Environment(ENV = os.environ, tools = ['Docs.Mkdocs'],
                    toolpath = [PyPackageDir('scons_tools_grbd.Tools')])
    setup_opts(env)

    # Use the first parameter as the mode to run as
    if len(COMMAND_LINE_TARGETS) > 0:
        cmd = COMMAND_LINE_TARGETS[0]
    else:
        print_useage(env)
        Exit(1)

    if cmd == 'serve':
        # Doxygen directory can get quite big, so iets remove it for serve mode
        doxydir = os.path.abspath('docs/doxygen')
        Execute(Delete(doxydir))
        tgt = env.MkdocsServer()
        Default(tgt)

    elif cmd == 'build':
        tgt = env.MkdocsBuild()
        Default(tgt)

    elif cmd == 'publish':
        tgt = env.MkdocsPublish("Site update")
        Default(tgt)

    elif cmd == 'clean':
        tgt = env.MkdocsBuild()
        Default(tgt)
        SetOption('clean', True)

    # Alternative Formats

    elif cmd == 'json':
        tgt = env.MkdocsJsonBuild()
        Default(tgt)

    elif cmd == 'mkcombine':
        tgt = env.MkdocsCombiner()
        Default(tgt)


    # TODO
    elif cmd == 'doxygen':
        print ("TODO doxygen_templates")

    # TODO
    elif cmd == 'pdf':
        manual_clean(env)
        markdown_target = env.MkdocsCombiner()
        pd_target = env.Pandoc('docs/export/site.pdf', markdown_target)
        Default(pd_target)

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
    print ("  doxygen       to build Doxygen related files to be inserted into the docs")
    print ("  pdf           to build the documentation as a pdf")



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
    #env.Replace(Mkdocs_Theme = 'cyborg')
    #env.Replace(Mkdocs_CleanBuild = True)
    #env.Replace(Mkdocs = 'mkdocs')
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
