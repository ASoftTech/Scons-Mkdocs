# MkdocsPublish

## Overview

This builder can be used to trigger Mkdocs into pushing the build output to the github pages branch.
This way it will be visible publicly.

Typically the output will be visible under something like

  * http://**OrganisationName**.github.io/**RepoName**

## Example useage:

```python
EnsureSConsVersion(3,0,0)
env = Environment(ENV = os.environ, tools = ['Docs.Mkdocs'], toolpath = [PyPackageDir('scons_tools_grbd.Tools')])
target = env.MkdocsPublish('commit message')
Default(target)
```

Optionally a source parameter can be passed to specify a different location of mkdocs.yml
```python
target = env.MkdocsPublish('commit message', 'someother.yml')
```

An example of changing a setting:

```python
env.Replace(Mkdocs_CleanBuild = True)
```


## Available Options

| env setting | Values | Description |
|-------------|--------|-------------|
| Mkdocs | 'mkdocs' | Override the executable / path to use |
| Mkdocs_WorkingDir | Current Directory | Can be set to override the working directory where mkdocs will be run |
| Mkdocs_CleanBuild | None (default), True, False | If to clean the build directory during the build (default is yes) |
| Mkdocs_RemoteBranch | None (default) | Override the remote branch name to use when pushing to github |
| Mkdocs_RemoteName | None (default) | Override the remote name to use when pushing to github |
| Mkdocs_ForcePush | False (default), True | Do a force push when pushing to github |
| Mkdocs_Quiet | False (default), True | Silence warnings |
| Mkdocs_Verbose | False (default), True | Enable verbose output |
| Mkdocs_ExtraArgs | [] (default) | Additional options to pass to mkdocs as an array |
