# Todo

## Module Path

Incorperate a ModulePath function into scons

https://stackoverflow.com/questions/729583/getting-file-path-of-imported-module
https://stackoverflow.com/questions/8380381/the-way-to-make-namespace-packages-in-python
https://packaging.python.org/guides/packaging-namespace-packages/


def showModulePath(module):
        if (hasattr(module, '__name__') is False):
            print 'Error: ' + str(module) + ' is not a module object.'
            return None


        moduleName = module.__name__
        modulePath = None
        if imp.is_builtin(moduleName):
            modulePath = sys.modules[moduleName];
        else:
            modulePath = inspect.getsourcefile(module)
            modulePath = '<module \'' + moduleName + '\' from \'' + modulePath + 'c\'>'
        print modulePath 
        return modulePath

setup scons to use entry points
https://stackoverflow.com/questions/774824/explain-python-entry-points
