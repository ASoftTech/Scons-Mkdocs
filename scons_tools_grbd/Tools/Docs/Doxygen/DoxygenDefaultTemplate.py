"""
DoxygenDefaultTemplate
  This tool will generate default template files for doxygen
"""

import os, sys, os.path as path
import SCons.Script
from SCons.Environment import Environment
from SCons.Script import Builder

# TODO fix relative imports when importing a single namespaced tool
from scons_tools_grbd.Tools.Docs.Doxygen import DoxygenCommon


def exists(env):
    """Check if we're okay to load this builder"""
    return DoxygenCommon.detect(env)


def generate(env):
    """Called when the tool is loaded into the environment at startup of script"""
    assert(exists(env))
    DoxygenCommon.setup_opts(env)

    doxyfile_scanner = env.Scanner(
        DoxygenCommon.DoxySourceScan,
        "DoxySourceScan",
        scan_check=DoxygenCommon.DoxySourceScanCheck,
    )

    #bld = Builder(action = __DoxygenDefaultTemplate_func, emitter = DoxygenCommon.DoxyEmitter,
    #    target_factory=env.fs.Entry, single_source=True,
    #    source_scanner=doxyfile_scanner)
    bld = Builder(action = __DoxygenDefaultTemplate_func, emitter = DoxygenCommon.DoxyEmitter,
        target_factory=env.fs.Entry, single_source=True)
    env.Append(BUILDERS = {'DoxygenDefaultTemplate' : bld})


def __DoxygenDefaultTemplate_func(target, source, env):
    """Actual builder that does the work after the Sconscript file is parsed"""
    cmdopts = ['$Doxygen']
    cmdopts += ["-w", "html"]

    # TODO targets
    cmdopts += ["theme/default/header.html", "theme/default/footer.html", "theme/default/customdoxygen.css"]

    cmdopts.append(str(source[0]))
    cmdopts = cmdopts + env['Doxygen_ExtraArgs']

    print('Building Doxygen default templates:')
    env.Execute(env.Action([cmdopts], chdir=env['Doxygen_WorkingDir']))
