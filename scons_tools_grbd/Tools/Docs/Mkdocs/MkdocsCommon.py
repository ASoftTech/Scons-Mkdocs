"""
MkdocsCommon
  Common code associated with mkdocs builders
"""

import os, sys, os.path as path, yaml
import SCons.Script
from SCons.Environment import Environment
from SCons.Script import File, Dir

def detect(env):
    """Detect if mkdocs exe is detected on the system, or use user specified option"""
    if 'Mkdocs' in env:
        return env.Detect(env['Mkdocs'])
    else:
        return env.Detect('mkdocs')


def detect_combiner(env):
    """Detect if mkdocscombine exe is detected on the system, or use user specified option"""
    if 'Mkdocs_Combine' in env:
        return env.Detect(env['Mkdocs_Combine'])
    else:
        return env.Detect('mkdocscombine')


def setup_opts(env):
    """Common setup of options for Mkdocs builders"""
    # Available Options - These override those within the yaml configuration file
    env.SetDefault(
        # Default exe to launch
        Mkdocs = 'mkdocs',
        # Working directory is current directory (default)
        Mkdocs_WorkingDir = env.Dir('.'),

        # If to Remove old files from the site_dir before building (the default).
        Mkdocs_CleanBuild = None,
        # If to enable Strict mode
        Mkdocs_Strict = False,
        # Which theme to use
        Mkdocs_Theme = None,
        # Directory of additional files to merge in with the theme
        Mkdocs_ThemeDir = None,
        # Directory to output the build to - default is 'site'
        Mkdocs_SiteDir = None,

        # If to override the default remote branch setting when uploading
        Mkdocs_RemoteBranch = None,
        # If to override the default remote name setting when uploading
        Mkdocs_RemoteName = None,
        # If to force the push to github
        Mkdocs_ForcePush = False,

        # Default is '127.0.0.1:8000'
        Mkdocs_ServeUrl = None,
        # If to use livereload, enabled by default
        # when pages change on the file system the browser auto refreshes to show the changes
        Mkdocs_LiveReload = None,
        # Enable the live reloading in the development server
        # but only re-build files that have changed
        Mkdocs_DirtyReload = False,

        # If to silence warnings
        Mkdocs_Quiet = False,
        # Show verbose messages
        Mkdocs_Verbose = False,
        # Additional Arguments
        Mkdocs_ExtraArgs = [],
        )


def setup_opts_combiner(env):
    """Common setup of options for Mkdocs combiner"""
    # Available Options - These override those within the yaml configuration file
    env.SetDefault(
        # File options

        # Default exe to launch
        Mkdocs_Combine = 'mkdocscombine',
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
        Mkdocs_Combine_PandocTables = None,
        # Width of generated grid tables in characters (default: 100)
        Mkdocs_Combine_TableWidth = None,

        # Link options

        # True = keep MkDocs-style cross-references, False = replace MkDocs-style cross-references by just their title (default)
        Mkdocs_Combine_Refs = None,
        # True = keep HTML anchor tags, False = strip out HTML anchor tags (default)
        Mkdocs_Combine_Anchors = None,

        # Extra options

        # True = combine the \( \) Markdown math into LaTeX $$ inlines, False = keep \( \) Markdown math notation as is (default)
        Mkdocs_Combine_MathLatex = None,
        # Extension to substitute image extensions by (default: no replacement)
        Mkdocs_Combine_ImageExt = None,
        # Additional Arguments
        Mkdocs_Combine_ExtraArgs = [],
        )


def MkdocsScanner(node, env, path, arg = None):
    """Dependency scanner for listing all files within the mkdocs source directory (typically docs)
    We exclude the doxygen dir since it has quite a lot of content and requires a clean build anyway
    Args:
        node: the SCons directory node to scan
        env:  the current SCons environment
        path: not used
        arg:  not used
    Returns:
        A list of files.
    """
    # Read mkdocs config
    yamlcfg, sitedirnode, docsdirnode = Mkdocs_Readconfig(node, env)
    # Look at the docs source directory
    searchpath = env.subst(docsdirnode.abspath)
    doxygen_path = os.path.join(searchpath, 'doxygen')
    depends = []
    for d, unused_s, files in os.walk(searchpath, topdown=True):
        if d.startswith(doxygen_path):
            continue
        for f in files:
            depends.append(File(os.path.join(d, f)))
    return depends


def Mkdocs_emitter(target, source, env):
    # Choose mkdocs.yml as source file if not specified
    if not source:
        cfgfile = File('mkdocs.yml')
        source.append(cfgfile)
    else:
        cfgfile = source[0]
    # Read mkdocs config
    yamlcfg, sitedirnode, docsdirnode = Mkdocs_Readconfig(cfgfile, env)
    # We need at least one target that's a file for the rebuild if source changes logic to work
    filenode = File(path.join(str(sitedirnode), 'mkdocs/search_index.json'))
    target.append(filenode)
    env.Clean(target, sitedirnode)
    return target, source


def MkdocsCombiner_emitter(target, source, env):
    # Choose mkdocs.yml as source file if not specified
    if not source:
        cfgfile = File('mkdocs.yml')
        source.append(cfgfile)
    else:
        cfgfile = source[0]
    # Read mkdocs config
    yamlcfg, sitedirnode, docsdirnode = Mkdocs_Readconfig(cfgfile, env)
    # Default target
    if not target:
        target = File(path.join(str(sitedirnode), 'export/mkdocs.pd'))
    return target, source


def Mkdocs_Readconfig(cfgfile, env):
    """Read the mkdocs yaml configuration file"""
    with open(str(cfgfile), 'r') as stream:
        yamlcfg = yaml.load(stream)
    # Determine destination site dir
    if env['Mkdocs_SiteDir']:
        sitedirnode = Dir(env['Mkdocs_SiteDir'])
    elif 'site_dir' in yamlcfg:
        sitedirnode = Dir(yamlcfg['site_dir'])
    else:
        sitedirnode = Dir('site')
    # Determind source docs dir
    if 'docs_dir' in yamlcfg:
        docsdirnode = Dir(yamlcfg['docs_dir'])
    else:
        docsdirnode = Dir('docs')
    return yamlcfg, sitedirnode, docsdirnode
