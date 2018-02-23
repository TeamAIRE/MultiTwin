#! /bin/bash

CWD=$(pwd)
echo -e "\nexport PATH=$CWD/python-scripts:\$PATH" >> ~/.profile
echo -e "\nexport PATH=$CWD/BlastProg:\$PATH" >> ~/.profile
echo -e "\nexport PYTHONPATH=$CWD/python-scripts:\$PYTHONPATH" >> ~/.profile
cd BlastProg/
make

