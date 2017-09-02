# Mkdocs2Pandoc

## Overview

This builder can be used to generate a file that can be imported into pandoc from mkdoc / markdown sources.
Pandoc can then be later used to generate a pdf or epub file from this .pd export file.

## Example useage:

```python
EnsureSConsVersion(3,0,0)
env = Environment(ENV = os.environ, tools = ['Docs.Mkdocs'], toolpath = [PyPackageDir('scons_tools_grbd.Tools')])
target = env.Mkdocs2Pandoc()
Default(target)
```

Optionally a source and target parameter can be passed to specify a different location for the mkdocs.yml and destination file
```python
target = env.Mkdocs2Pandoc('docs/site.pd', 'someother.yml')
```

An example of changing a setting:

```python
env.Replace(Mkdocs_Pandoc_Width = 100)
```


## Available Options

| env setting | Values | Description |
|-------------|--------|-------------|
| Mkdocs2pandoc | 'mkdocs2pandoc' | Override the executable / path to use |
| Mkdocs_WorkingDir | Current Directory | Can be set to override the working directory where mkdocs will be run |
| Mkdocs_Pandoc_Encoding | None (default) | Can be used to override the encoding for input files (default is utf-8) |
| Mkdocs_Pandoc_ImageExt | None (default) | Extension to substitute image extensions by (default: no replacement) |
| Mkdocs_Pandoc_Width | None (default) | Width of generated grid tables in characters (default: 100) |
| Mkdocs_Pandoc_Exclude | None (default) | Include files to skip (default: none) |
| Mkdocs_ExtraArgs | [] (default) | Additional options to pass to mkdocs as an array |
