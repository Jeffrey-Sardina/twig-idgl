#!/bin/bash

#Update package list
apt-get update

#Note that liblapack-dev, libblas-dev, and gfortran are needed for scipy as noted in: https://techoverflow.net/2018/12/31/fixing-numpy-distutils-system_info-notfounderror-no-lapack-blas-resources-found-on-ubuntu-or-travis/
echo 'installing python, pip, git, and other packages'
apt-get install -y python3.7 python3-pip git liblapack-dev libblas-dev gfortran

#Ready to install the IDGL dependencies now
echo 'installing from requirements.txt'
pip install -r IDGL/requirements.txt
