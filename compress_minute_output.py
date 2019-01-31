import glob
import sys
import os
sys.path.append('/users/jvergara/python_code')
import Jesuslib_eth as jle
import numpy as np
import time
from netCDF4 import Dataset
path='output/'+sys.argv[1]+'/6min_precip/'
os.chdir(path)

files=glob.glob('lffd??????????????.nc')
#print(files)
files=np.sort(files)
start_day=files[0].split('/')[-1][4:-3]
end_day=files[-1].split('/')[-1][4:-3]
print (start_day)
print (end_day)
daily_list=jle.Daily_time_list(start_day,end_day)
#print(daily_list)

for day in daily_list:
    t1=time.time()
    print(day)
    if len(glob.glob('lffd'+day+'??????.nc'))<240:
        print('--------------------------------------------------------------')
        print('--------------------------------------------------------------')
        print('Output from day '+day+' not completed. Original files mantained')
        print('--------------------------------------------------------------')
        print('--------------------------------------------------------------')
        continue

    if os.path.isfile('day_lffd'+day+'.nc'):
        if Dataset('day_lffd'+day+'.nc').dimensions["time"].size==240:
            print('compresed file exists and have the right time dimensions, skipping')
            continue

    cmd='cdo cat lffd'+day+'??????.nc day_lffd'+day+'.nc'

    out=os.system(cmd)
    print(out)
    if not out and Dataset('day_lffd'+day+'.nc').dimensions["time"].size==240:
        os.system('rm -rf lffd'+day+'??????.nc')
    elif Dataset('day_lffd'+day+'.nc').dimensions["time"].size>240:
        raise NameError('Nota all output is available or data concatenated more than once')
    t2=time.time()
    print(t2-t1)
    #break


