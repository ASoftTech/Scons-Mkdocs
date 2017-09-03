# MkdocsCombiner

## Overview

This builder can be used to generate a file that can be imported into pandoc from mkdoc / markdown sources.
Pandoc can then be later used to generate a pdf or epub file from this .pd export file.
The output file is basically a combination of all pages into a single markdown file.

Note to get this to work you'll need to install from git since mkdocs-combiner isn't currently published on pypi.
```
pip install git+https://github.com/twardoch/mkdocs-combine.git
```


## Example useage:

```python
EnsureSConsVersion(3,0,0)
env = Environment(ENV = os.environ, tools = ['Docs.Mkdocs'], toolpath = [PyPackageDir('scons_tools_grbd.Tools')])
target = env.MkdocsCombiner()
Default(target)
```

Optionally a source and target parameter can be passed to specify a different location for the mkdocs.yml and destination file
```python
target = env.MkdocsCombiner('docs/site.pd', 'someother.yml')
```

An example of changing a setting:

```python
env.Replace(Mkdocs_Pandoc_Width = 100)
```


## Available Options

### File Options

| env setting | Values | Description |
|-------------|--------|-------------|
| Mkdocs_Combine | 'mkdocscombine' | Override the executable / path to use |
| Mkdocs_WorkingDir | Current Directory | Can be set to override the working directory where mkdocs will be run |
| Mkdocs_Combine_Encoding | None (default) | Can be used to override the encoding for input files (default is utf-8) |
| Mkdocs_Combine_Exclude | None (default) | Include files to skip (default: none) |
| Mkdocs_Combine_OutputHtml | False (default), True | If to output a single html page instead of markdown |

### Structure options

| env setting | Values | Description |
|-------------|--------|-------------|
| Mkdocs_Combine_Meta | None (default), True, False | If to keep YAML metadata (default), False = strip YAML metadata |
| Mkdocs_Combine_Titles | None (default), True, False | Add titles from mkdocs.yml to Markdown files (default), False = do not add titles to Markdown files |
| Mkdocs_Combine_Uplevels | None (default), True, False | Increase ATX header levels in Markdown files (default), False = do not increase ATX header levels in Markdown files |

### Table options

| env setting | Values | Description |
|-------------|--------|-------------|
| Mkdocs_Combine_PandocTables | None (default), True, False | True = keep original Markdown tables (default), False = combine Markdown tables to Pandoc-style grid tables |
| Mkdocs_Combine_TableWidth | None (default) | Width of generated grid tables in characters (default: 100) |

### Link options

| env setting | Values | Description |
|-------------|--------|-------------|
| Mkdocs_Combine_Refs | None (default), True, False | True = keep MkDocs-style cross-references, False = replace MkDocs-style cross-references by just their title (default) |
| Mkdocs_Combine_Anchors | None (default), True, False | True = keep HTML anchor tags, False = strip out HTML anchor tags (default) |

### Extra options

| env setting | Values | Description |
|-------------|--------|-------------|
| Mkdocs_Combine_MathLatex | None (default), True, False | True = combine the \( \) Markdown math into LaTeX $$ inlines, False = keep \( \) Markdown math notation as is (default) |
| Mkdocs_Combine_ImageExt | None (default) | Extension to substitute image extensions by (default: no replacement) |
| Mkdocs_Combine_ExtraArgs | [] (default) | Additional options to pass to mkdocs as an array |
