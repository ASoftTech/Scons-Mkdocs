"""
Dll2Lib
  This tool will generate a .lib file under windows for a given .dll file
  This uses dumpfile to export a list of symbols
      dumpbin /exports C:\yourpath\yourlib.dll
  The list of symbols is then written to a .def file
  The lib command is then used to generate the .lib file from the .def file
      lib /def:C:\mypath\mylib.def /OUT:C:\mypath\mylib.lib
  A side affect of this is an .exp file which also requires cleanup
  We can then use the .lib file for linking with the compiler under Windows
"""

import os, sys, os.path as path, subprocess
import SCons.Script
from SCons.Environment import Environment
from SCons.Script import *
from SCons.Tool.MSCommon import msvc_exists, msvc_setup_env_once


def exists(env):
    return msvc_exists()


def generate(env):
    """Called when the tool is loaded into the environment at startup of script"""
    assert(exists(env))

    # Set-up ms tools paths
    msvc_setup_env_once(env)

    env.SetDefault(
        # Location of the dumpbin executable
        DUMPBIN = 'dumpbin',
    )

    # Register the builder
    bld = Builder(action = __Dll2Lib_func, emitter = __Dll2Lib_emitter)
    env.Append(BUILDERS = {'Dll2Lib' : bld})


def __Dll2Lib_emitter(target, source, env):
    """Add the generated .def and .exp files to the list of targerts for cleanup"""
    addfiles = []
    for item in target:
        libfile = item.abspath
        deffile = path.splitext(libfile)[0] + '.def'
        expfile = path.splitext(libfile)[0] + '.exp'
        addfiles.append(File(deffile))
        addfiles.append(File(expfile))
    target = target + addfiles
    return target, source


def __Dll2Lib_func(target, source, env):
    """Actual builder that does the work after the Sconscript file is parsed"""
    index = 0
    for srcitem in source:
        srcfile = str(srcitem)
        filename = str(target[index])
        libfile = path.splitext(filename)[0] + '.lib'
        deffile = path.splitext(filename)[0] + '.def'
        if path.splitext(srcfile)[1] != '.dll':
            continue
        dumpbin_exp = __dumpbin_run_exports(env, srcfile)
        exportlist = __dumpbin_parse_exports(dumpbin_exp)
        __write_deffile(deffile, exportlist)
        __generate_lib(env, deffile, libfile)
        index = index + 1


def __dumpbin_run_exports(env, dllfile):
    """Run dumpbin /exports against the input dll"""
    cmdopts = [env['DUMPBIN'], '/exports', str(dllfile)]
    print("Calling '%s'" % env['DUMPBIN'])
    stdout, stderr = __runcmd_mbcs(env, cmdopts)
    return stdout


def __dumpbin_parse_exports(input):
    """Parse thr output from dumpbin as a list of symbols"""
    ret = []
    lines = input.split('\n')
    for line in lines:
        arr1 = line.split()
        if len(arr1) == 4 and arr1[1] != 'number' and arr1[1] != 'hint':
            ret.append(arr1[3])
    return ret


def __write_deffile(outfile, lines):
    """Write the list of symbols to a .def file"""
    with open(outfile, 'w') as f:
        f.write('EXPORTS\n')
        for line in lines:
            f.write(line + '\n')


def __generate_lib(env, deffile, libfile):
    """Generate the .lib file"""
    cmdopts = [env['AR'], '/def:' + deffile, '/OUT:' + libfile]
    stdout, stderr = __runcmd_mbcs(env, cmdopts)
    return stdout


def __runcmd_mbcs(env, cmdopts):
    """Run command while capturing the output"""
    popen = SCons.Action._subproc(env, cmdopts, stdin='devnull',
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout = popen.stdout.read()
    stderr = popen.stderr.read()

    if not isinstance(stderr, str):
        stderr = stderr.decode("mbcs")
    if not isinstance(stdout, str):
        stdout = stdout.decode("mbcs")

    if stderr:
        import sys
        sys.stderr.write(stderr)
    if popen.wait() != 0:
        raise IOError(stderr)
    return stdout, stderr
