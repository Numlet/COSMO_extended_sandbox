#!/bin/tcsh
#SBATCH --job-name=compressing
#SBATCH --output=compresing_job.out
#SBATCH --nodes=1
#SBATCH --partition=normal
#SBATCH --time=03:30:00
#SBATCH --account=pr94
#SBATCH --constraint=gpu

python compress_minute_output.py $1
