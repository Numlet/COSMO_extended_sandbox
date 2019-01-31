#!/bin/bash -l
#
#SBATCH --time=12:00:00
#SBATCH --job-name=sync_out
#SBATCH --output=sync_out.out
#SBATCH --ntasks=1
#SBATCH --partition=xfer

module unload xalt
command="rsync -aq"
echo -e "$SLURM_JOB_NAME started on $(date):\n $command $1 $2\n"
$command $1 $2
echo -e "$SLURM_JOB_NAME finished on $(date)\n"

