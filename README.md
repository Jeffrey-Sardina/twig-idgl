# TWIG-IGDL

## Project Notes and Credits
TWIG is the **T**wig **W**izard for **I**ntelligence **G**eneration. It is currently in development by Jeffrey Sardina (ORCID ID https://orcid.org/0000-0003-0654-2938) as a part of his PhD work at Trinity College Dublin.

This version of TWIG makes use of IDGL, a GNN library developed by Chen et al, for GNN training. Its license can be found in the folder IDGL/LICENSE. As per the license terms "You must cause any modified files to carry prominent notices stating that You changed the files", all modified or add files in the IDGL folder have been clearly marked as modified or added. A list of all added, modified, and deleted files can also be found under the Directory Contents subheading in this README file. 

TWIG also uses HpBandSter, a hyperparameter optimization package that implements (among other algorithms) BOHB (Bayesian optimization HyperBand) as in "BOHB: Robust and Efficient Hyperparameter Optimization at Scale". It is made available under a BSD 3-Clause License.

IDGL Citation
- Yu Chen, Lingfei Wu and Mo hammed J. Zaki. "Iterative Deep Graph Learning for Graph Neural Networks: Better and Robust Node Embeddings." In Proceedings of the 34th Conference on Neural Information Processing Systems (NeurIPS 2020), Dec 6-12, 2020.

BOHB citation:
@InProceedings{falkner-icml-18,
  title =        {{BOHB}: Robust and Efficient Hyperparameter Optimization at Scale},
  author =       {Falkner, Stefan and Klein, Aaron and Hutter, Frank},
  booktitle =    {Proceedings of the 35th International Conference on Machine Learning},
  pages =        {1436--1445},
  year =         {2018},
}


## LICENSE
As per the IDGL license, "You may add Your own copyright statement to Your modifications and may provide additional or different license terms and conditions for use, reproduction, or distribution of Your modifications, or for any such Derivative Works as a whole, provided Your use,       reproduction, and distribution of the Work otherwise complies with the conditions stated in this License."

All modifications to the IDGL work (be they in the IDGL directory or outside of it) and all other TWIG work is placed under a different license. Please see the LICENSE file in the document root for these license details.

## Directory Contents
(folders)
- **config/** -- a folder containing bash scripts used to configure the container. The data in this folder is used directly in the container as a volume. This is done using the bash script:
    - **install.sh** -- installs IDGL and all its dependencies (such as miniconda, Python, and Torch)
- **data/** -- a folder containing custom datasets for use with IDGL that do not come with it be default. The data in this folder is used directly in the container as a volume. It is kept separate from IDGL/data/ to avoid modifying the original project where possible.
- **GNN_module/** -- a repo cloned from https://github.com/hugochan/IDGL. The data in this folder is used directly in the container as a volume. The modifications made to this project are as follows:
    - requirements.txt -- remove torch install command, as a newer version is needed to support more modern GPUs and is installed separately. This version should now support RTX 30XX, and is verified to run on the RTX 3080-TI.
- **NAS_module/** -- code for implementing NAS and hyperparameter optimisation, currently running on TPE from https://github.com/jaberg/hyperopt/tree/master
- **twig_module/** -- code for TWIG commands and Twig container setup. Twig is invoked via twig.py, which by default reads from a configuration file named TwigJob for determining what jobs and workflows to run.

(files)
- **docker-compose.yml** -- a Docker compose file that governs container creation for this module. The GNN is run only in a container, not on the base OS, to make this as reproducible and simple as possible.
- **LICENSE** -- the license for  this work
- **README.md** -- this document 

## Instructions and Troubleshooting
To start Twig-IDGL
- at the project root, run ```$ docker-compose up```
- open a terminal session in the container (for example, through the "Remote - Containers" extension in Visual Studio Code)
- inside the container, run
    - ```$ cd /workspace/twig_module/```
    - ```$ conda activate pyenv```
    - ```$ ./twig.py --do_your_job TwigJob.yml > twig_out```

Verifying that everything works as expected
- When the output prints "**************** MODEL CONFIGURATION ****************", ensure that the tag  "[ Using CUDA ]" appears below -- if not, the model will be running on CPU, not GPU, and take far too long to complete.
    - If this does not print, then ensure that you have NVIDIA drivers set up on your host machine (see here; on Windows 11 this seems to be done automatically, but it may require manual steps on Ubuntu: https://docs.docker.com/config/containers/resource_constraints/#gpu)
- You can also run ```$ nvidia-smi``` in the container to verify that the container is able to see your NVIDIA hardware drivers on your host machine. If it cannot this could mean one if two things:
    - You do not have an NVIDIA GPU (if this is the case, this container will not work for you)
    - Your NVIDIA GPU cannot be seen by Docker (not sure why this would happen if you followed the above steps)
