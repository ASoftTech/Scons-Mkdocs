@echo off
SETLOCAL

IF EXIST "virtualenv_py3" (
    echo "Entering virtual environment virtualenv_py3"
    cmd /k "virtualenv_py3\Scripts\activate.bat"

) ELSE (
    echo "Creating virtual environment virtualenv_py3"
    SET WORKON_HOME=.
    mkvirtualenv --python=C:\Python35\python.exe virtualenv_py3
    cmd /k "virtualenv_py3\Scripts\activate.bat & pip install -r requirements_py3.txt"
)

ENDLOCAL