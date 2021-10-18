This directory contains:
(folders)
- config/ -- a folder containing bash scripts used to configure the container (install python, iniconda, git, and IDGL). This is done in two files:
    - install_python.sh -- installs python, miniconda (a python package manager) and git (for downloading GitHub repositories)
    - install_idgl.sh -- uses git to clone the IDGL repo. Then, conda installs all necessary dependencies (such as torch and numpy) that are needed to run IDGL
- data/ -- a folder containing custom datasets for use with IDGL that do not come with it be default.
- IDGL_clone/ -- a repo cloned from https://github.com/hugochan/IDGL. I currently have this for future purposes only; the Docker container simply pulls from GitHub to always be using the latest version, making this folder unnecessary

(files)
- docker-compose.yml -- a Docker compose file that governs container creation for this module. The GNN is run only in a container, not on the base OS, to make this as reproducible and simple as possible.
- README.md -- this document