# Dll2Lib

## Overview

This builder can be used to generate a lib file from a dll. <br>
The lib file can then be linked into an existing project. <br>
This uses dumpfile to export a list of symbols:

Typically:
```
dumpbin /exports C:\yourpath\yourlib.dll
```

The list of symbols is then written to a .def file. <br>
The lib command is then used to generate the .lib file from the .def file
```
lib /def:C:\mypath\mylib.def /OUT:C:\mypath\mylib.lib
```
A side affect of this is an .exp file which also requires cleanup


## Example useage:

```python
EnsureSConsVersion(3,0,0)
env = Environment(ENV = os.environ, tools = ['default', 'MSBuild'], toolpath = [PyPackageDir('scons_tools_grbd.Tools')])
target = env.Dll2Lib('D:\\Temp\\SomeDll.dll')
Default(target)
```

Optionally a target parameter can be passed to specify a different location of the destination .lib file
```python
target = env.Dll2Lib('D:\\Temp\\test1.lib', 'D:\\Temp\\SomeDll.dll')
```

An example of changing a setting:

```python
env.Replace(DUMPBIN = 'dumpbin')
```


## Available Options

| env setting | Values | Description |
|-------------|--------|-------------|
| DUMPBIN | 'dumpbin' | Override the executable / path to use |
