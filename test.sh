
cd
rm -rf /scratch/snx3000/jvergara/cosmo_sandbox_test
git clone cosmo_sandobox_x_chain /scratch/snx3000/jvergara/cosmo_sandbox_test
cd /scratch/snx3000/jvergara/cosmo_sandbox_test
python define_simulation.py
python control_simulation.py
cp /store/c2sm/pr04/jvergara/base_executables/* bin/
./run_daint.sh
