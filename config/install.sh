#!/bin/bash

#Update package list
apt-get update

#Install conda
apt-get install -y wget
if [[ ! -d "/root/miniconda3" ]]
then
    wget https://repo.anaconda.com/miniconda/Miniconda3-py38_4.10.3-Linux-x86_64.sh
    chmod u+x Miniconda3-py38_4.10.3-Linux-x86_64.sh
    ./Miniconda3-py38_4.10.3-Linux-x86_64.sh -b
    rm Miniconda3-py38_4.10.3-Linux-x86_64.sh
fi
export PATH=$PATH:~/miniconda3/bin
conda create -n "pyenv" python=3.7 pip
conda run --no-capture-output -n pyenv pip install -r IDGL/requirements.txt

#Install IDGL packages
# pip install -r IDGL/requirements.txt

# #Note that liblapack-dev, libblas-dev, and gfortran are needed for scipy as noted in: https://techoverflow.net/2018/12/31/fixing-numpy-distutils-system_info-notfounderror-no-lapack-blas-resources-found-on-ubuntu-or-travis/
# echo 'installing python, pip, git, and other packages'
# apt-get install -y python=3.7
# apt-get install -y python3-pip #git liblapack-dev libblas-dev gfortran

# # #Ready to install the IDGL dependencies now
# # echo 'installing from requirements.txt'
# pip install -r IDGL/requirements.txt
