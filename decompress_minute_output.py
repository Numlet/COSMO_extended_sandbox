import glob
import sys
import os
sys.path.append('/users/jvergara/python_code')
import Jesuslib_eth as jle
import numpy as np
from netCDF4 import Dataset
path='output/'+sys.argv[1]+'/6min_precip/'
os.chdir(path)

files=np.sort(glob.glob('day_lffd*'))
#print(files)

for file_name in files:
    print(file_name)
    cmd='cdo splitsel,1 '+file_name+' single_file_'+file_name[:-3]
    print(cmd)
    out=os.system(cmd)
    print(out)
    temp_files=glob.glob('single_file_'+file_name[:-3]+'*')
    temp_files=np.sort(temp_files)
    #print([name for name in Dataset(temp_files[0]).history.split(' ') if name[:4]=='lffd'])
    original_names=[name for name in Dataset(temp_files[0]).history.split(' ') if name[:4]=='lffd']
    original_names=np.sort(list(set(original_names)))
    print(len(original_names),len(temp_files))
    if not len(temp_files)==len(original_names):
        raise NameError('NOT SAME AMOUNT OF FILES AS ORIGINALLY CONCATENADED!!!')
    for i in range(len(original_names)):
        #print('renaming ', temp_files[i],' to ', original_names[i])
        cmd='mv '+temp_files[i]+' '+original_names[i]
        #print(cmd)
        out=os.system(cmd)
        if not out:os.system('rm -rf '+temp_files[i])
        else:raise NameError('Error when renaming files')
    os.system('rm -rf '+file_name) 


