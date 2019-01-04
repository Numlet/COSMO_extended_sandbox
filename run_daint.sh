#!/bin/bash
#cp /store/c2sm/pr04/jvergara/base_executables/* bin/

module load craype-accel-nvidia60

export MALLOC_MMAP_MAX_=0
export MALLOC_TRIM_THRESHOLD_=536870912
export OMP_NUM_THREADS=1
export CDO_EXEC=/apps/daint/UES/jenkins/6.0.UP04/gpu/easybuild/software/CDO/1.9.0-CrayGNU-17.08/bin/cdo

ulimit -s unlimited
ulimit -a
module load daint-gpu
export MPICH_RDMA_ENABLED_CUDA=1


while getopts "o" opt
   do
     case $opt in
        o ) export IO_REDUCED="yes";;
     esac
done
# global setup
export SCHEDULER="SLURM"
export QUEUE="normal"
export ACCOUNT="pr04"
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

export LM_YYYY_BEGIN=1998
export LM_MM_BEGIN=09
export LM_DD_INI=01
export LM_ZZ_BEGIN=${LM_ZZ_INI}

export LM_NL_HSTART=42360
export LM_NL_HSTOP=43080

export FRONTS_TS_START=2006060100
export FRONTS_TS_END=2006060200

# launch jobs
jobid=""
lmfid=""
pwd
#parts="0_get_data 1_ifs2lm 2_lm_c 3_lm2lm 4_lm_f 5_trajectories 6_climate_analysis 7_msd 8_front_tracking"
parts="0_get_data 1_ifs2lm 2_lm_c 3_lm2lm 4_lm_f"
parts="3_lm2lm 4_lm_f"
parts="2_lm_c"
#parts="1_ifs2lm 2_lm_c"
parts="1_ifs2lm 2_lm_c"
#parts='1_ifs2lm'
#parts="1_ifs2lm"
#parts='0_get_data'
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
  cd - 1>/dev/null 2>/dev/null
done
