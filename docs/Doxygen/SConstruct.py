# These import lines are not really needed, but it helps intellisense within VS when editing the script
import SCons.Script
from SCons.Environment import Environment

import sys, os

# Set PYTHONPATH before using if running without scons_tools_grbd installed via pip

def main():
    # Setup environment
    EnsureSConsVersion(3,0,0)
    env = Environment(ENV = os.environ, tools = ['Docs.Doxygen', 'Docs.Mkdocs'],
                     toolpath = [PyPackageDir('scons_tools_grbd.Tools')])
    setup_opts(env)

    # Use the first parameter as the mode to run as
    if len(COMMAND_LINE_TARGETS) > 0:
        cmd = COMMAND_LINE_TARGETS[0]
    else:
        print_useage(env)
        Exit(1)

    if cmd == 'build':
        tgt = env.Doxygen('Doxyfile')
        Default(tgt)
        # TODO Copy theme/search.js   to Mkdocs/docs/doxygen/search/search.js
        # TODO Copy theme/doxygen.css to Mkdocs/docs/doxygen/doxygen.css
        # print ("Build finished. The HTML pages are in " + self.BUILDDIR)
        pass

    elif cmd == 'template_mkdocs':
        # TODO
        pass

    elif cmd == 'template_def':
        #tgt = env.DoxygenDefaultTemplate('Doxyfile')
        #Default(tgt)
        # TODO
        pass

    elif cmd == 'clean':
        #tgt = env.MkdocsBuild()
        #Default(tgt)
        #SetOption('clean', True)
        pass


    # 1. clean build of Mkdocs
    # 2. launch template_mkdocs in the doxygen script to regenerate the headers
    # 3. clear the docs/doxygen directory
    # 4. run the doxygen script in build mode





    else:
        print_useage(env)
        Exit(1)


def print_useage(env):
    print ("Please use scons <target> where <target> is one of")
    print ("  build         to build the documentation as HTML files")


def setup_opts(env):
    """Optionally change the default options"""
    env.Replace(Doxygen_BuildDir = Dir('#../Mkdocs/docs/doxygen'))


main()

# Ignore the command line and just use default targets
SCons.Script.BUILD_TARGETS = DEFAULT_TARGETS
