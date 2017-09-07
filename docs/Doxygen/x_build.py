# MkDocs Build Script
class MkDocsBuild(object):

    # Class Init
    def __init__(self):
        self.SRCDIR = "Docs"
        self.BUILDDIR = "site"
        self.DOXYDIR = "../Doxygen"
        self.DOXYBUILDDIR = "../Doxygen/html"
        self.MKDOCSDIR = "./"

    # Build the Doxygen Files
    def build_doxygen(self):
        # Do a build of the site so we can extract the top menu
        cmdopts = ["mkdocs", "build", "--clean"]
        self.run_cmd(cmdopts, self.MKDOCSDIR)

        # Re-create the doxygen templates
        print("Building Doxygen templates")
        cmdopts = ["python", "build.py", "template_mkdocs"]
        self.run_cmd(cmdopts, self.DOXYDIR)

        # Clean the doxygen output dir
        self.emptydir("Docs/doxygen")
        if os.path.exists(os.path.abspath("Docs/doxygen")):
            os.rmdir(os.path.abspath("Docs/doxygen"))

        # Run Doxygen
        print("Building Doxygen Files")
        cmdopts = ["python", "build.py", "build"]
        self.run_cmd(cmdopts, self.DOXYDIR)

