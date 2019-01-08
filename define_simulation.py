#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 13:52:48 2018

@author: jvergara
"""

import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import os.path
import os
import sys
import numpy as np
# =============================================================================
# Define chain for simulation
# =============================================================================
name_run='test_'+str(datetime.datetime.now().time())
name_run='soil_spin_up_test_22-06-2018'
name_run='GA_run_5min_precip'

copy=True
if copy:
    os.system('cp ~/sync_out.sh .')
store_system='/store/c2sm/pr04/jvergara/RUNS_IN_SCRATCH/'
saving_folder=store_system+name_run+'/'

#Initial date
LM_YYYY_INI='1993'
LM_MM_INI='11'
LM_DD_INI='10'
LM_ZZ_INI='00'

#end of chained dates
LM_YYYY_END_CHAIN='1993'
LM_MM_END_CHAIN='11'
LM_DD_END_CHAIN='14'
LM_ZZ_END_CHAIN='00'


main_simulation_step='2_lm_c'
main_simulation_step='4_lm_f'

d_ini=datetime.datetime(int(LM_YYYY_INI),int(LM_MM_INI),int(LM_DD_INI),int(LM_ZZ_INI))

d_end_chain=datetime.datetime(int(LM_YYYY_END_CHAIN),int(LM_MM_END_CHAIN),int(LM_DD_END_CHAIN),int(LM_ZZ_END_CHAIN))


months_per_step=1

def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month

months_in_between=diff_month(d_end_chain,d_ini)
steps=months_in_between/months_per_step

if months_in_between%months_per_step:
    raise NameError('Number of months is not divisible by the specified months per step')


days_per_step=1
last_step=0
def diff_days(d1, d2):
    return (d1-d2).days
if days_per_step:
    days_in_between=diff_days(d_end_chain,d_ini)
    steps=days_in_between/days_per_step
    if days_in_between%days_per_step:
        last_step=days_in_between%days_per_step
    
def get_dt(step=main_simulation_step):
    with open(step+'/run') as f: lines = f.read().splitlines()
    num=np.nan
    for line in lines:
        if line.startswith('DT='):
            num = float(line.split('=')[-1].strip()[:])
            print (num)
    return num

def get_idbg(step=main_simulation_step):
    with open(step+'/run') as f: lines = f.read().splitlines()
    num=np.nan
    for line in lines:
        if line.startswith('  idbg_level ='):
            num = int(float(line.split('=')[-1].strip()[:-1]))
            print (num)
    return num

def multiply_idbg(n=10,step=main_simulation_step):
    number=get_idbg(step=step)
    new_number=number*n
    a=os.system("sed -i 's/  idbg_level = %i/  idbg_level = %i/g' %s/run"%(number,new_number,step))


def time():
    return datetime.datetime.now().strftime('%y/%m/%d-%H:%M:%S')






dt=get_dt()
idbg=get_idbg()

columns=['step','start_date', 'end_date', 'h_str', 'h_end', 'status','dt','idbg_level','last_update']
name_control_dataframe='Dataframe_'+name_run
# =============================================================================
# Create chain
# =============================================================================
if __name__=='__main__':
    os.makedirs(saving_folder, exist_ok=True)
    if not os.path.isfile(name_control_dataframe):
        print('Creating dataframe')
        dataframe=pd.DataFrame(columns=columns)
        
        d_end=d_ini
        for i in range(int(steps)):
            d_str=d_end
            if not days_per_step:
                d_end=d_end+ relativedelta(months=months_per_step)
            else:
                d_end=d_end+ relativedelta(days=days_per_step)
                
            h_str=(d_str-d_ini).days*24
            h_end=(d_end-d_ini).days*24
            status=0
            run_setup = pd.DataFrame([[i,d_str.isoformat()[:10],d_end.isoformat()[:10],h_str,h_end,status,dt,idbg,time()]], columns=columns)
            dataframe=dataframe.append(run_setup)
        if last_step:
            d_str=d_end
            d_end=d_end+ relativedelta(days=last_step)
            h_str=(d_str-d_ini).days*24
            h_end=(d_end-d_ini).days*24
            status=0
            run_setup = pd.DataFrame([[int(steps),d_str.isoformat()[:10],d_end.isoformat()[:10],h_str,h_end,status,dt,idbg,time()]], columns=columns)
            dataframe=dataframe.append(run_setup)
            
            
        dataframe.to_csv(name_control_dataframe,mode = 'w',sep="\t", index=False)
    else:
        print("Dataframe was already created")
