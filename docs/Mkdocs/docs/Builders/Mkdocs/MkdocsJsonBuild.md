# MkdocsJsonBuild

## Overview

This builder can be used to trigger Mkdocs into building the source markdown into a json output on disk.
This can be used as an import into other tools.


## Example useage:

```python
EnsureSConsVersion(3,0,0)
env = Environment(ENV = os.environ, tools = ['Docs.Mkdocs'], toolpath = [PyPackageDir('scons_tools_grbd.Tools')])
target = env.MkdocsJsonBuild()
Default(target)
```

Optionally a source parameter can be passed to specify a different location of mkdocs.yml
```python
target = env.MkdocsJsonBuild('someother.yml')
```

An example of changing a setting:

```python
env.Replace(Mkdocs_CleanBuild = True)
env.Replace(Mkdocs_Strict = True)
```


## Available Options

| env setting | Values | Description |
|-------------|--------|-------------|
| Mkdocs | 'mkdocs' | Override the executable / path to use |
| Mkdocs_WorkingDir | Current Directory | Can be set to override the working directory where mkdocs will be run |
| Mkdocs_CleanBuild | None (default), True, False | If to clean the build directory during the build (default is yes) |
| Mkdocs_Strict | False (default), True | If to use mkdocs in strict mode |
| Mkdocs_SiteDir | 'site' (default) | This setting controls the output directory for the html to be rendered |
| Mkdocs_Quiet | False (default), True | Silence warnings |
| Mkdocs_Verbose | False (default), True | Enable verbose output |
| Mkdocs_ExtraArgs | [] (default) | Additional options to pass to mkdocs as an array |
