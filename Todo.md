# Todo

## General

  * Test cleanup in all instances
  * write more tests
  * look at https://bitbucket.org/scons/scons/wiki/ToolsIndex
  * look at https://bitbucket.org/scons/scons/wiki/ContributedBuilders

  * Once scons moves to github file a new issue
    a tool requires an exists function, it's searched for but never actually called.
    so we end up having to call it from within the generate function.
    Based on some of the mails from a couple of years ago there's plans to change the tool mechansim.
  * Take another look at relative imports within the tool loader

## Entry Points

setup scons to use entry points
https://stackoverflow.com/questions/774824/explain-python-entry-points
http://amir.rachum.com/blog/2017/07/28/python-entry-points/


## Builders

### MkdocsCombiner

  * Account for arrays / lists in the exclusion list

### Pandoc

  * Add additional options for formatting

### Doxygen

  * roll in support for doxygen via a builder
    https://bitbucket.org/russel/scons_doxygen/src

### Dll2Lib

  * check over this and
    D:\SourceControl\GitRepos.Appst\Gtk3-Sharp-Core\site_scons\site_tools
    D:\SourceControl\GitRepos.Appst\Gbd.Scons.Extensions
    for additional tools / code