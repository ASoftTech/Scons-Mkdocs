"""
MkdocsCombiner
  This tool uses mkdocscombiner to generate a pd file which can then be used with pandoc to generate a pdf or other forms of documentation
"""

import os, sys, os.path as path
import SCons.Script
from SCons.Environment import Environment
from SCons.Script import *


def _detect(env):
    if 'Mkdocs_Combine' in env:
        return env['Mkdocs_Combine']
    return env.Detect("mkdocscombine")

def exists(env):
    return _detect(env)


def generate(env):
    """Called when the tool is loaded into the environment at startup of script"""
    assert(exists(env))
    # Available Options - These override those within the yaml configuration file
    env.SetDefault(

        # File options

        # Working directory is current directory (default)
        Mkdocs_WorkingDir = env.Dir('.'),
        # Set encoding for input files (default: utf-8)
        Mkdocs_Combine_Encoding = None,
        # Include files to skip (default: none)
        Mkdocs_Combine_Exclude = None,
        # If to output a single html page instead of markdown
        Mkdocs_Combine_OutputHtml = False,

        # Structure options

        # If to keep YAML metadata (default), False = strip YAML metadata
        Mkdocs_Combine_Meta = None,
        # Add titles from mkdocs.yml to Markdown files (default), False = do not add titles to Markdown files
        Mkdocs_Combine_Titles = None,
        # Increase ATX header levels in Markdown files (default), False = do not increase ATX header levels in Markdown files
        Mkdocs_Combine_Uplevels = None,

        # Table options

        # True = keep original Markdown tables (default), False = combine Markdown tables to Pandoc-style grid tables
        Mkdocs_Combine_PandocTables = None
        # Width of generated grid tables in characters (default: 100)
        Mkdocs_Combine_TableWidth = None,

        # Link options

        # True = keep MkDocs-style cross-references, False = replace MkDocs-style cross-references by just their title (default)
        Mkdocs_Combine_Refs = None
        # True = keep HTML anchor tags, False = strip out HTML anchor tags (default)
        Mkdocs_Combine_Anchors = None

        # Extra options

        # True = combine the \( \) Markdown math into LaTeX $$ inlines, False = keep \( \) Markdown math notation as is (default)
        Mkdocs_Combine_MathLatex = None,
        # Extension to substitute image extensions by (default: no replacement)
        Mkdocs_Combine_ImageExt = None,
        # Additional Arguments
        Mkdocs_Combine_ExtraArgs = [],
        )

    # Register the builder
    bld = Builder(action = __MkdocsCombiner_func)
    env.Append(BUILDERS = {'__MkdocsCombiner' : bld})
    env.AddMethod(MkdocsCombiner, 'MkdocsCombiner')


def MkdocsCombiner(env, target = None, source = None):
    """Wrapper for the Builder so that we can use a default on the source parameter"""
    if not source:
        source = File('mkdocs.yml')
    if not target:
        target = File('docs/site.pd')
    return env.__MkdocsCombiner(target, source)


def __MkdocsCombiner_func(target, source, env):
    """Actual builder that does the work after the Sconscript file is parsed"""
    cmdopts = [_detect(env)]

    index = 0
    for srcitem in source:
        cfgfile = str(srcitem)
        outfile = str(target[index])

        if cfgfile:
            cmdopts.append('--config-file=' + cfgfile)

        if env['Mkdocs_Combine_OutputHtml']:
            cmdopts.append('--outhtml' + outfile)
        else:
            cmdopts.append('--outfile=' + outfile)

        # File options

        if env['Mkdocs_Combine_Encoding']:
            cmdopts.append('--encoding=' + str(env['Mkdocs_Combine_Encoding']))

        # TODO parse list as input
        if env['Mkdocs_Combine_Exclude']:
            cmdopts.append('--exclude=' + str(env['Mkdocs_Combine_Exclude']))

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
            cmdopts.append('--grid-width=' + str(env['Mkdocs_Combine_TableWidth']))

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
            cmdopts.append('--image-ext=' + str(env['Mkdocs_Combine_ImageExt']))

        cmdopts = cmdopts + env['Mkdocs_Combine_ExtraArgs']

        print('Building MkDocs Documentation as combined markdown file:')
        env.Execute(env.Action([cmdopts], chdir=env['Mkdocs_WorkingDir']))
        index = index + 1
