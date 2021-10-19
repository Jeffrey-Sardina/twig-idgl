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

#Install IDGL
export PATH=$PATH:~/miniconda3/bin
conda create -n "pyenv" python=3.7 pip
conda run --no-capture-output -n pyenv pip install -r IDGL/requirements.txt
conda run --no-capture-output -n pyenv pip install torch==1.9.1+cu111 torchvision==0.10.1+cu111 torchaudio==0.9.1 -f https://download.pytorch.org/whl/torch_stable.html
conda init bash #new
