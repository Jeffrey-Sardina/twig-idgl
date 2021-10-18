This directory contains:
(folders)
- config/ -- a folder containing bash scripts used to configure the container (installing python, git, and IDGL). The data in this folder is used directly in the container as a volume. This is done in two files:
    - install.sh -- installs IDGL and all its dependencies (such as Python and Torch)
- data/ -- a folder containing custom datasets for use with IDGL that do not come with it be default. The data in this folder is used directly in the container as a volume
- IDGL/ -- a repo cloned from https://github.com/hugochan/IDGL, with some modifications made. The data in this folder is used directly in the container as a volume

(files)
- docker-compose.yml -- a Docker compose file that governs container creation for this module. The GNN is run only in a container, not on the base OS, to make this as reproducible and simple as possible.
- README.md -- this document