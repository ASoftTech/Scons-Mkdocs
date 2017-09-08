import os.path, os
import TestSCons

test = TestSCons.TestSCons()

test.dir_fixture('images/MkdocsJsonBuild')
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
__MkdocsJsonBuild_func(["mkdocs", "site2\mkdocs\search_index.json"], ["mkdocs.yml", "docs\index.md"])
Building MkDocs Documentation as Json:
mkdocs json --config-file=mkdocs.yml --site-dir=site2
__MkdocsJsonBuild_func(["site\mkdocs\search_index.json"], ["mkdocs.yml", "docs\index.md"])
Building MkDocs Documentation as Json:
mkdocs json --config-file=mkdocs.yml --clean --strict --site-dir=site --quiet --verbose
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
