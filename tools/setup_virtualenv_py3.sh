#! /bin/bash

if [ ! -d "virtualenv_py3" ]; then
  echo "Creating virtual environment virtualenv_py3"
  virtualenv --python=/usr/bin/python3.5 virtualenv_py3
  source virtualenv_py3/bin/activate
  pip install -r requirements_py3.txt
fi

# Enter the python virtual enviro on the current shell
echo "Entering virtual environment virtualenv_py3"
bash --rcfile <(echo '. virtualenv_py3/bin/activate')

# use echo $BASHPID to check the bash prompt process id

