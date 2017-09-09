# vim: set et sw=3 tw=0 fo=awqorc ft=python:
# -*- mode:python; coding:utf-8; -*-
#
# Astxx, the Asterisk C++ API and Utility Library.
# Copyright © 2005, 2006  Matthew A. Nicholson
# Copyright © 2006  Tim Blechmann
#
#  Copyright © 2007 Christoph Boehme
#
#  Copyright © 2012 Dirk Baechle
#
#  Copyright © 2013 Russel Winder
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License version 2.1 as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

# The original version was tested with doxygen 1.4.6

import os, sys, os.path as path
import SCons.Script
from SCons.Environment import Environment
from SCons.Script import Builder

# TODO fix relative imports when importing a single namespaced tool
from scons_tools_grbd.Tools.Docs.Doxygen import DoxygenCommon


def exists(env):
    """Check if we're okay to load this builder"""
    return DoxygenCommon.detect(env)


def generate(env):
    """Called when the tool is loaded into the environment at startup of script"""
    assert(exists(env))
    DoxygenCommon.setup_opts(env)

    doxyfile_scanner = env.Scanner(
        DoxygenCommon.DoxySourceScan,
        "DoxySourceScan",
        scan_check=DoxygenCommon.DoxySourceScanCheck,
    )

    bld = Builder(action = __Doxygen_func, emitter = DoxygenCommon.DoxyEmitter,
        target_factory=env.fs.Entry,
        source_scanner=doxyfile_scanner)
    env.Append(BUILDERS = {'Doxygen' : bld})


def __Doxygen_func(target, source, env):
    """Actual builder that does the work after the Sconscript file is parsed"""
    cmdopts = ['$Doxygen']
    cmdopts.append(str(source[0]))
    cmdopts = cmdopts + env['Doxygen_ExtraArgs']

    print('Building Doxygen html:')
    env.Execute(env.Action([cmdopts], chdir=env['Doxygen_WorkingDir']))
