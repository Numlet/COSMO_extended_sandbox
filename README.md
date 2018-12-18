# README

## COSMO installation

Tutorial located at https://github.com/PallasKat/buildenv/wiki/Build-COSMO-POMPA

## Setup the python environment

To install the python environment with miniconda, use the `install.sh` script in `pythonenv`

    cd pythonenv
 
To see all available option
 
    ./install.sh -h
    
To install with the defaults and installing a module and append the path to your bashrc

    ./install.sh -i -a
    
You can then do the following to activate environment

    module load miniconda
    source activate dyn
