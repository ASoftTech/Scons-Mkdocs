# MkdocsServer

## Overview

This builder can be used to trigger Mkdocs into server mode.
This is useful when you want a preview of the site that will be built before publishing it live to github pages.

During server mode mkdocs pulls all the markdown and images into memory before rendering it as a http server.
Typically via the link of

  * <http://127.0.0.1:8000>

With live reload enabled (which is the default) and changes make to the markdown files will auto trigger a reload of the web page
to reflect any changes made.

One example use case of the MkdocsServer builder would be to have other builders change the source //docs// directory
(such as importing doxygen generated files)
Before triggering the MkdocsServer builder to then serve out the page as a preview.
This could be done via the scons dependency mechanism.

## Example useage:

```python
EnsureSConsVersion(3,0,0)
env = Environment(ENV = os.environ, tools = ['Docs.Mkdocs'], toolpath = [PyPackageDir('scons_tools_grbd.Tools')])
target = env.MkdocsServer()
Default(target)
```

Optionally a source parameter can be passed to specify a different location of mkdocs.yml
```python
target = env.MkdocsServer('someother.yml')
```

An example of changing a setting:

```python
env.Replace(Mkdocs_ServeUrl = '127.0.0.1:8001')
env.Replace(Mkdocs_Strict = True)
```


## Available Options

| env setting | Values | Description |
|-------------|--------|-------------|
| Mkdocs | 'mkdocs' | Override the executable / path to use |
| Mkdocs_WorkingDir | Current Directory | Can be set to override the working directory where mkdocs will be run |
| Mkdocs_ServeUrl | None, '127.0.0.1:8000' (default) | The server URL to use when hosting the page |
| Mkdocs_Strict | False (default), True | If to use mkdocs in strict mode |
| Mkdocs_Theme | None (default), 'cyborg' | This setting can be used to override the theme specified within mkdocs.yml |
| Mkdocs_ThemeDir | None (default), 'theme' | This setting can be used to override / specify a theme directory to overlay files on top of the selected theme |
| Mkdocs_LiveReload | None (default), True, False | If to enable / disable the live reload on change of source markdown (default in on) |
| Mkdocs_DirtyReload | False (default), True | If to enable dirty reload mode |
| Mkdocs_Quiet | False (default), True | Silence warnings |
| Mkdocs_Verbose | False (default), True | Enable verbose output |
| Mkdocs_ExtraArgs | [] (default) | Additional options to pass to mkdocs as an array |
