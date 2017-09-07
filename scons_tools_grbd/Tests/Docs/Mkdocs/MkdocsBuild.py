#!/usr/bin/env python
#
# __COPYRIGHT__
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

__revision__ = "__FILE__ __REVISION__ __DATE__ __DEVELOPER__"

import os.path, os
import TestSCons

test = TestSCons.TestSCons()

test.dir_fixture('images/MkdocsBuild')
test.run(arguments = '.', stdout = None, stderr = None)

stdout_filtered = []
for line in test.stdout().splitlines():
    if 'os.chdir' not in line:
        stdout_filtered.append(line)
stdout_filtered = os.linesep.join(stdout_filtered)

expected_stdout = """\
scons: Reading SConscript files ...
scons: done reading SConscript files.
scons: Building targets ...
__MkdocsBuild_func(["mkdocs", "site2\mkdocs\search_index.json"], ["mkdocs.yml", "docs\index.md"])
Building MkDocs Documentation:
mkdocs build --config-file=mkdocs.yml --theme=cyborg --theme-dir=theme --site-dir=site2
__MkdocsBuild_func(["site\mkdocs\search_index.json"], ["mkdocs.yml", "docs\index.md"])
Building MkDocs Documentation:
mkdocs build --config-file=mkdocs.yml --clean --strict --theme=cyborg --theme-dir=theme --site-dir=site --quiet --verbose
scons: done building targets.
"""
expected_stdout = os.linesep.join(expected_stdout.splitlines())

#test.diff(expected_stdout, stdout_filtered, 'STDOUT ')
assert stdout_filtered == expected_stdout
test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
