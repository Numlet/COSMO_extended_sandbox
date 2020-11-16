# COSMO Extended Sandbox
Extended version of the Sandbox to run the COSMO chain

## Requirements
This code is prepared to run at Piz Daint from the login nodes. The only **extra requirement** is to have **python3** installed, preferable with minconda. 

## Code structure
The code is structured in different steps that need to be executed to simulate the standard chain

*0_get_data: Scripts to copy automatically ERA or MPI files
*1_ifs2lm: Generate 12km boundary conditions from GCM or reanalysis fields. 
*2_lm_c: Run Cosmo at 12km. 
*3_lm2lm: Generate high resolution boundary conditions for the nested run. 
*4_lm_f: Run cosmo at high-resolution (standard 2.2km)
*x_chain: Check that the simulation step has correctly been performed and resubmit the next step.  

## Simple set up to run chained simulations

1-Copy the cosmo and int2lm executables into the bin/ folder. The current standard executables can be found in /store/c2sm/pr04/jvergara/base_executables

2-Edit define_simulation.py to set the steps of the simulation.

3-Run it with `python define_simulation.py`

4-Run `python control_simulation.py` which will set the values needed for running the next step

5-Check that in run_daint.sh the "parts" variable contains the steps necessary for the simulation and that the last step is x_chain (if you want to automatically chain your simulation)

6-Execute `./run_daint`

7-Enjoy! 

