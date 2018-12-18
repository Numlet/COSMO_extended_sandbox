#!/usr/bin/env bash

exitError()
{
	echo "ERROR $1: $3" 1>&2
	echo "ERROR     LOCATION=$0" 1>&2
	echo "ERROR     LINE=$2" 1>&2
	exit "$1"
}


showUsage()
{ 
	echo "Install miniconda and dyn environment"
	echo ""

	echo "USAGE:"
	usage="$(basename "$0") [-p path] [-v path] [-m path] [-a] [-i] [-f]"

	echo "${usage}"
	echo ""
	echo "-h	Show this help"
	echo ""
	echo "Optional arguments, see default:"
	echo "-p	The install path, default to ${SCRATCH}/miniconda"
	echo "-v	The path to the virtualenvs, default to ${SCRATCH}/virtualenvs"
	echo "-i	Install a module for miniconda, defaults to OFF"
	echo "-m 	The path to the module directory, default to ${HOME}/modules"
	echo "-a	Add modulepath to ${HOME}/.bashrc, defaults OFF"
	echo "-f 	Force the re-installation of miniconda and the conda environment"
	
}


# set defaults and process command line options
parseOptions()
{ 
	local OPTIND
	installpath=${SCRATCH}/miniconda
	virtualenvpath=${SCRATCH}/virtualenvs
        modulepath=${HOME}/modules
        addtoRc=OFF
        installModule=OFF
	mforce=""
	cforce=""

	while getopts "hp:v:m:aif" opt; do
		case "${opt}" in
		h) 
		    showUsage
		    exit 0 
		    ;;
		p) 
		    installpath=$OPTARG 
		    ;;
		v)
		    virtualenvpath=$OPTARG
		    ;;
		m)
		    modulepath=$OPTARG
	            ;;
		a)
		    addtoRc=ON
		    ;;
		i)
		    installModule=ON
		    ;;
		f)
		   mforce="-f"
		   cforce="--force"
		   ;;
		\?) 
		    showUsage
		    exitError 601 ${LINENO} "invalid command line option (-${OPTARG})"
		    ;;
		esac
	done
	shift $((OPTIND-1))
}


installModule()
{
  mkdir -p ${modulepath} || exitError 620 ${LINENO} "Unable to create the module directory"
  cat > ${modulepath}/miniconda <<module_EOF
#%Module

module-whatis "Provides conda and a python environment for crCLIM"

set	version		0.1
setenv	CONDA_ENVS_PATH		${virtualenvpath}/
prepend-path	PATH		${installpath}/miniconda/bin
module_EOF
  if [ ${addtoRc} == "ON" ]; then
  	echo -e "# Add path to local module\nexport MODULEPATH=\$MODULEPATH:${modulepath}" | tee -a ${HOME}/.bashrc ||exitError 622 ${LINENO} "Unable to add modulepath to bashrc"
  fi
}


# ===================================================
# MAIN LIKE
# ===================================================

# parse command line options (pass all of them to function)
parseOptions "$@"

currentdir=$(dirname $(realpath $0))

wget -c http://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O $currentdir/Miniconda3-latest-Linux-x86_64.sh || exitError 611 ${LINENO} "Unable to download Miniconda"

bash $currentdir/Miniconda3-latest-Linux-x86_64.sh ${mforce} -b -p ${installpath} || exitError 612 ${LINENO} "Unable to install Miniconda"

export PATH=${installpath}/bin:$PATH

export CONDA_ENVS_PATH=${virtualenvpath}


module unload PrgEnv-cray
module load PrgEnv-gnu
conda env create -f $currentdir/dyn.yml -q ${cforce} || exitError 613 ${LINENO} "Unable to create the dyn environment"

if [ ${installModule} == "ON" ]; then
	installModule $currentdir
fi




