# Readme

This directory contains some scripts for the setup of a python virtual environment.
This can be used for development purposes to setup everything needed to run the code.


## Building Development scons

In order to use the latest master version of scons instead of the one installed via pip <br>
We can download and build scons via:

Under Windows:
```
hg clone https://grbd@bitbucket.org/grbd/scons scons-test
cd scons-test
C:\Python35\python.exe bootstrap.py build/scons
cd ..
```

Under Linux:
```
hg clone https://grbd@bitbucket.org/grbd/scons scons-test
cd scons-test
python3 bootstrap.py build/scons
cd ..
```

## Python virtual environment

Next to setup a python virtual environment.

For Windows:
```
setup_virtualenv_py3.bat
```
For Linux:
```
setup_virtualenv_py3.sh
```

This will create a python virtual environment within the virtualenv_py3 directory.
Any tools required will be installed at this point via pip / the reading in of **requirements_py3.txt**

To create a new requirements_py3.txt after instaling some additional tools
```
pip freeze > requirements_py3.txt
```


## Installing Scons into the virtual environment

To install scons within the python virtual environment we can use the following

First make sure we're in the python virtual environment
```
setup_virtualenv_py3.bat
```

To install the version of scons we've built
```
pip install --egg scons-test\build\scons
```

Currently scons 2.5.1 doesn't support the PyPackageDir function so in the above examples
I'm currently using a development version of the code

A couple of notes

  * It looks as if we can't use the -e option when using pip with scons
  * Also we need to build the source before installing with pip, so we can't install directory from source control.
