# MkDocs Build Script
class MkDocsBuild(object):

    # Class Init
    def __init__(self):
        self.SRCDIR = "Docs"
        self.BUILDDIR = "site"
        self.DOXYDIR = "../Doxygen"
        self.DOXYBUILDDIR = "../Doxygen/html"
        self.MKDOCSDIR = "./"


    # Empty a directory
    def emptydir(self, top):
        if(top == '/' or top == "\\"): return
        else:
            for root, dirs, files in os.walk(top, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))

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

    # Do the main build
    def build(self):
        self.clean()
        print("Building MkDocs Files")
        cmdopts = ["mkdocs", "build", "--clean"]
        self.run_cmd(cmdopts, self.MKDOCSDIR)
        print ("Build finished. The HTML pages are in " + self.BUILDDIR)

    # Publish the Site
    def publish(self):
        self.build()
        print("Publishing MkDocs Files")
        cmdopts = ["mkdocs", "gh-deploy"]
        self.run_cmd(cmdopts, self.MKDOCSDIR)
        print ("Publish finished.")

    # Clean the Build directory
    def clean(self):
        self.emptydir("site")
        print ("Clean finished")

    def main(self):
        if len(sys.argv) != 2:
            self.usage()
            return
        if sys.argv[1] == "build":
            self.build()
        if sys.argv[1] == "build_doxygen":
            self.build_doxygen()
        if sys.argv[1] == "clean":
            self.clean()
        if sys.argv[1] == "publish":
            self.publish()

if __name__ == "__main__":
    MkDocsBuild().main()
