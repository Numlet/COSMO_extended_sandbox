# README

## Extended version of the Sandbox to run the COSMO chain

## Setup and run a chained simulation

1-Copy the executables into the bin/ folder. The current standard executables can be found in /store/c2sm/pr04/jvergara/base_executables

2-Edit define_simulation.py to set the steps of the simulation.

3-Run it with "python define_simulation.py"

4-Run "python control_simulation.py" which will set the values needed for running the next step

5-Check that in run_daint.sh the "parts" variable contains the steps necessary for the simulation and that the last step is x_chain (if you want to automatically chain your simulation)

6-Execute "./run_daint"

7-Enjoy! 

