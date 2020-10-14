#!/bin/bash
#cp /store/c2sm/pr94/jvergara/base_executables/* bin/

#module use /apps/common/UES/sandbox/kraushm/easybuild/dom-CLE7.19.09/modules/all
module load daint-gpu

#module load COSMO_pompa/31d7227-CrayCCE-19.08-cuda-10.0-crclim-double
#module unload cudatoolkit
#module load cudatoolkit/10.0.130_3.22-7.0.1.0_5.2__gdfb4ce5

export MV2_ENABLE_AFFINITY=0
export MV2_USE_CUDA=1
export MPICH_RDMA_ENABLED_CUDA=1
export MPICH_G2G_PIPELINE=256


while getopts "o" opt
   do
     case $opt in
        o ) export IO_REDUCED="yes";;
     esac
done
# global setup
NAME_RUN="testing_sandbox"

export SCHEDULER="SLURM"
export QUEUE="debug"
export ACCOUNT="pr94"
export RUNCMD="srun"
export CORES_PER_NODE=24
export TASKS_PER_NODE=1
export GPUS_PER_NODE=1
export CONDA_ENVS_PATH=/scratch/snx3000/npiaget/virtualenvs/

# setup configurations
export NPX_IFS2LM=3
export NPY_IFS2LM=6
export NPIO_IFS2LM=0
export EXE_IFS2LM="./int2lm"

export NPX_LMC=2
export NPY_LMC=2
export NPIO_LMC=0
export EXE_LMC="./lm_f90"

export NPX_LM2LM=6
export NPY_LM2LM=10
export NPIO_LM2LM=0
export EXE_LM2LM="./int2lm"

export NPX_LMF=5
export NPY_LMF=5
export NPIO_LMF=4
export EXE_LMF="./lm_f90"

# Configure Simulation
export LM_YYYY_INI=1993
export LM_MM_INI=11
export LM_DD_INI=01
export LM_ZZ_INI=00

export LM_YYYY_BEGIN=1993
export LM_MM_BEGIN=11
export LM_DD_INI=01
export LM_ZZ_BEGIN=${LM_ZZ_INI}

export LM_NL_HSTART=0
export LM_NL_HSTOP=24

export FRONTS_TS_START=2006060100
export FRONTS_TS_END=2006060200

# launch jobs
jobid=""
lmfid=""
pwd

parts="0_get_data 1_ifs2lm 2_lm_c 3_lm2lm 4_lm_f x_chain"

for part in ${parts} ; do
  short=`echo "${part}" | sed 's/^[0-9]*_//g'`
  number=${part%%_*}
  echo "launching ${short}"
  #\rm -rf output/${short} 2>/dev/null
  mkdir -p output/${short}
  cd ${part}
  jobid=`./run ${SCHEDULER} ${QUEUE} ${ACCOUNT} ${jobid}`
  if [[ $number -eq 4 ]];
   then
    lmfid=$jobid
  elif [[ $number -ge 5 ]];
   then
    jobid=$lmfid
  fi
  echo "${short} ${jobid}"
  
  cd - 1>/dev/null 2>/dev/null
done
