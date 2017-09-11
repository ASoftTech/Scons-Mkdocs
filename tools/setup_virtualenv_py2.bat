@echo off
SETLOCAL

IF EXIST "virtualenv_py2" (
    echo "Entering virtual environment virtualenv_py2"
    cmd /k "virtualenv_py2\Scripts\activate.bat"

) ELSE (
    echo "Creating virtual environment virtualenv_py2"
    SET WORKON_HOME=.
    mkvirtualenv --python=C:\Python27\python.exe virtualenv_py2
    cmd /k "virtualenv_py2\Scripts\activate.bat & pip install -r requirements_py2.txt"
)

ENDLOCAL