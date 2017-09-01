# MkdocsBuild

## Overview

This builder can be used to trigger Mkdocs into building the source markdown into a html output on disk.
This is typically the sort of thing you would do before publishing the html content to a site.


## Example useage:

```python
EnsureSConsVersion(3,0,0)
env = Environment(ENV = os.environ, tools = ['Docs.Mkdocs'], toolpath = [PyPackageDir('scons_grbd_docs.Tools')])
target = env.MkdocsBuild()
Default(target)
```

Optionally a source parameter can be passed to MkdocsServer to specify a different location of mkdocs.yml
```python
target = env.MkdocsBuild('someother.yml')
```

An example of changing a setting:

```python
env.Replace(Mkdocs_CleanBuild = True)
env.Replace(Mkdocs_Strict = True)
```


## Available Options

| env setting | Values | Description |
|-------------|--------|-------------|
| Mkdocs_WorkingDir | Current Directory | Can be set to override the working directory where mkdocs will be run |
| Mkdocs_CleanBuild
| Mkdocs_Strict | False (default), True | If to use mkdocs in strict mode |
| Mkdocs_Theme | None (default), 'cyborg' | This setting can be used to override the theme specified within mkdocs.yml |
| Mkdocs_ThemeDir | None (default), 'theme' | This setting can be used to override / specify a theme directory to overlay files on top of the selected theme |
| Mkdocs_SiteDir | 'site' (default) | This setting controls the output directory for the html to be rendered |
| Mkdocs_Quiet | False (default, True | Silence warnings |
| Mkdocs_Verbose | False (default), True | Enable verbose output |
| Mkdocs_ExtraArgs | [] (default) | Additional options to pass to mkdocs as an array |
