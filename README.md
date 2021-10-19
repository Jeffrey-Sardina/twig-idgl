# TWIG-IGDL

## Project Notes and Credits
This project makes use of IDGL, a GNN library developed by Chen et al. Its license can be found in the folder IDGL/LICENSE. As per the license terms "You must cause any modified files to carry prominent notices stating that You changed the files", all modified or add files in the IDGL folder have been clearly marked as modified or added. A list of all added, modified, and deleted files can also be found under the Directory Contents subheading in this README file. 

IDGL Citation
- Yu Chen, Lingfei Wu and Mohammed J. Zaki. "Iterative Deep Graph Learning for Graph Neural Networks: Better and Robust Node Embeddings." In Proceedings of the 34th Conference on Neural Information Processing Systems (NeurIPS 2020), Dec 6-12, 2020.

## LICENSE
As per the IDGL license, "You may add Your own copyright statement to Your modifications and may provide additional or different license terms and conditions for use, reproduction, or distribution of Your modifications, or for any such Derivative Works as a whole, provided Your use,       reproduction, and distribution of the Work otherwise complies with the conditions stated in this License."

All modifications to the IDGL work (be they in the IDGL directory or outside of it) are placed under a different license. Please see the LICENSE file in the document root for these license details.

## Directory Contents
(folders)
- **config/** -- a folder containing bash scripts used to configure the container. The data in this folder is used directly in the container as a volume. This is done using the bash script:
    - **install.sh** -- installs IDGL and all its dependencies (such as miniconda, Python, and Torch)
- **data/** -- a folder containing custom datasets for use with IDGL that do not come with it be default. The data in this folder is used directly in the container as a volume. It is kept separate from IDGL/data/ to avoid modifying the original project where possible.
- **IDGL/** -- a repo cloned from https://github.com/hugochan/IDGL. The data in this folder is used directly in the container as a volume. The modifications made to this project are as follows:
    - none

(files)
- **docker-compose.yml** -- a Docker compose file that governs container creation for this module. The GNN is run only in a container, not on the base OS, to make this as reproducible and simple as possible.
- **README.md** -- this document

## Instructions and Troubleshooting
To start Twig-IDGL
- at the project root, run ```$ docker-compose up```
- open a terminal session in the container (for example, through the "Remote - Containers" extension in Visual Studio Code)
- inside the container, run
    - ```$ cd /workspace/IDGL/src/```
    - ```$ conda activate pyenv```
    - ```$ python main.py -config config/cora/idgl.yml```

Verifying that everything works as expected
- When the output prints "**************** MODEL CONFIGURATION ****************", ensure that the tag  "[ Using CUDA ]" appears below -- if not, the model will be running on CPU, not GPU, and take far too long to complete.
    - If this does not print, then ensure that you have NVIDIA drivers set up on your host machine (see here; on Windows 11 this seems to be done automatically, but it may require manual steps on Ubuntu: https://docs.docker.com/config/containers/resource_constraints/#gpu)
- You can also run ```$ nvidia-smi``` in the container to verify that the container is able to see your NVIDIA hardware drivers on your host machine. If it cannot this could mean one if two things:
    - You do not have an NVIDIA GPU (if this is the case, this container will not work for you)
    - Your NVIDIA GPU cannot be seen by Docker (not sure why this would happen if you followed the above steps)
