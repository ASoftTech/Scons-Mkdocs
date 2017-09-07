"""
MkdocsCombiner
  This tool uses mkdocscombiner to generate a pd file which can then be used with pandoc to generate a pdf or other forms of documentation
"""

import os, sys, os.path as path
import SCons.Script
from SCons.Environment import Environment
from SCons.Script import Builder


# TODO fix relative imports when importing a single namespaced tool
from scons_tools_grbd.Tools.Docs.Mkdocs import MkdocsCommon


def exists(env):
    """Check if we're okay to load this builder"""
    return MkdocsCommon.detect_combiner(env)


def generate(env):
    """Called when the tool is loaded into the environment at startup of script"""
    assert(exists(env))
    MkdocsCommon.setup_opts_combiner(env)
    bld = Builder(action = __MkdocsCombiner_func, emitter = MkdocsCommon.MkdocsCombiner_emitter)
    env.Append(BUILDERS = {'MkdocsCombiner' : bld})


def __MkdocsCombiner_func(target, source, env):
    """Actual builder that does the work after the Sconscript file is parsed"""
    cmdopts = ['$Mkdocs_Combine']
    cmdopts.append('--config-file=' + str(source[0]))
    if env['Mkdocs_Combine_OutputHtml']:
        cmdopts.append('--outhtml=' + str(target[0]))
    else:
        cmdopts.append('--outfile=' + str(target[0]))

    # File options
    if env['Mkdocs_Combine_Encoding']:
        cmdopts.append('--encoding=$Mkdocs_Combine_Encoding')
    # TODO parse list as input
    if env['Mkdocs_Combine_Exclude']:
        cmdopts.append('--exclude=$Mkdocs_Combine_Exclude')

    # Structure options
    if env['Mkdocs_Combine_Meta'] == True:
        cmdopts.append('--meta')
    elif env['Mkdocs_Combine_Meta'] == False:
        cmdopts.append('--no-meta')
    if env['Mkdocs_Combine_Titles'] == True:
        cmdopts.append('--titles')
    elif env['Mkdocs_Combine_Titles'] == False:
        cmdopts.append('--no-titles')
    if env['Mkdocs_Combine_Uplevels'] == True:
        cmdopts.append('--up-levels')
    elif env['Mkdocs_Combine_Uplevels'] == False:
        cmdopts.append('--keep-levels')

    # Table options
    if env['Mkdocs_Combine_PandocTables'] == True:
        cmdopts.append('--grid-tables')
    elif env['Mkdocs_Combine_PandocTables'] == False:
        cmdopts.append('--tables')
    if env['Mkdocs_Combine_TableWidth']:
        cmdopts.append('--grid-width=$Mkdocs_Combine_TableWidth')

    # Link options
    if env['Mkdocs_Combine_Refs'] == True:
        cmdopts.append('--refs')
    elif env['Mkdocs_Combine_Refs'] == False:
        cmdopts.append('--no-refs')
    if env['Mkdocs_Combine_Anchors'] == True:
        cmdopts.append('--anchors')
    elif env['Mkdocs_Combine_Anchors'] == False:
        cmdopts.append('--no-anchors')

    # Extra options
    if env['Mkdocs_Combine_MathLatex'] == True:
        cmdopts.append('--latex')
    elif env['Mkdocs_Combine_MathLatex'] == False:
        cmdopts.append('--math')
    if env['Mkdocs_Combine_ImageExt']:
        cmdopts.append('--image-ext=$Mkdocs_Combine_ImageExt')
    cmdopts = cmdopts + env['Mkdocs_Combine_ExtraArgs']

    print('Building MkDocs Documentation as combined markdown file:')
    env.Execute(env.Action([cmdopts], chdir=env['Mkdocs_WorkingDir']))
