
cd
rm -rf /scratch/snx3000/jvergara/cosmo-pompa_x_chain_v1.1_test
git clone cosmo-pompa_x_chain_v1.1 /scratch/snx3000/jvergara/cosmo-pompa_x_chain_v1.1_test
cd /scratch/snx3000/jvergara/cosmo-pompa_x_chain_v1.1_test/cosmo/test/climate/crClim2km_DVL
python define_simulation.py
python control_simulation.py
cp /store/c2sm/pr04/jvergara/base_executables/* bin/
./run_daint.sh
