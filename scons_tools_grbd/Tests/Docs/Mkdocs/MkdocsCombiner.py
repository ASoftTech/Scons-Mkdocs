import os.path, os
import TestSCons

test = TestSCons.TestSCons()

test.dir_fixture('images/MkdocsCombiner')
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
__MkdocsCombiner_func(["site\mkdocs.pd"], ["mkdocs.yml", "docs\index.md"])
Building MkDocs Documentation as combined markdown file:
mkdocscombine --config-file=mkdocs.yml --outfile=site\mkdocs.pd
scons: done building targets.
"""
expected_stdout = os.linesep.join(expected_stdout.splitlines())

if stdout_filtered == expected_stdout:
    test.pass_test()
else:
    test.diff(expected_stdout, stdout_filtered, 'STDOUT ')
    test.fail_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
