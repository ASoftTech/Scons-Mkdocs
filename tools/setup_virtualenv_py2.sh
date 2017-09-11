#! /bin/bash

if [ ! -d "virtualenv_py2" ]; then
  echo "Creating virtual environment virtualenv_py2"
  virtualenv --python=/usr/bin/python2.7 virtualenv_py2
  source virtualenv_py2/bin/activate
  pip install -r requirements_py2.txt
fi

# Enter the python virtual enviro on the current shell
echo "Entering virtual environment virtualenv_py2"
bash --rcfile <(echo '. virtualenv_py2/bin/activate')

# use echo $BASHPID to check the bash prompt process id

