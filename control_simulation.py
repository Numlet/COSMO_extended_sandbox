#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 09:25:39 2018

@author: jvergara
"""

import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import os.path
import os
import sys
from define_simulation import d_ini, d_end_chain,name_control_dataframe, saving_folder,copy, get_dt,main_simulation_step, time, get_idbg,multiply_idbg
pd.options.mode.chained_assignment = None

def edit_and_submit_run(d_ini,d_str,h_str,h_end):
    #Init dates
    a=os.system("sed -i 's/.*LM_YYYY_INI.*/export LM_YYYY_INI=%i/' run_daint.sh"%d_ini.year)
    if a:return 1
    a=os.system("sed -i 's/.*LM_MM_INI.*/export LM_MM_INI=%02.i/' run_daint.sh"%d_ini.month)
    if a:return 1
    a=os.system("sed -i 's/.*LM_DD_INI.*/export LM_DD_INI=%02.i/' run_daint.sh"%d_ini.day)
    if a:return 1
    #Begin dates
    a=os.system("sed -i 's/.*LM_YYYY_BEGIN.*/export LM_YYYY_BEGIN=%i/' run_daint.sh"%d_str.year)
    if a:return 1
    a=os.system("sed -i 's/.*LM_MM_BEGIN.*/export LM_MM_BEGIN=%02.i/' run_daint.sh"%d_str.month)
    if a:return 1
    #Start and end date
    a=os.system("sed -i 's/.*LM_NL_HSTART.*/export LM_NL_HSTART=%i/' run_daint.sh"%h_str)
    if a:return 1
    a=os.system("sed -i 's/.*LM_NL_HSTOP.*/export LM_NL_HSTOP=%i/' run_daint.sh"%h_end)
    if a:return 1
#    a=os.system("sed -i 's/.*do.*/do=1opt/' run_daint.sh"%h_end)
#    os.mknod(str(d_str))
#    os.system("sbatch chain_simulation.sh")
    if os.path.isfile('2_lm_c/job.out'): 
        a=os.system('cp 2_lm_c/job.out job.lm_c.out.%s'%d_str.isoformat()[:10])
        a=os.system('cp 2_lm_c/job.out 2_lm_c/job.lm_c.out.%s'%d_str.isoformat()[:10])
    else:
        print('2_lm_c/job.out file did not exist')
    if os.path.isfile('4_lm_f/job.out'):
        a=os.system('cp 4_lm_f/job.out job.lm_f.out.%s'%d_str.isoformat()[:10])
        a=os.system('cp 4_lm_f/job.out 4_lm_f/job.lm_f.out.%s'%d_str.isoformat()[:10])
    else:
        print('4_lm_f/job.out file did not exist')
    #a=os.system('./run_daint.sh')
    print ('Ready to run next step!!')
    return 0

def closer_5(number):
    if number%5>2.5:
        number=number- number%5+5
    else:
        number=number- number%5
    return number


def create_datetime(string):
    d=datetime.datetime(int(string[:4]),int(string[5:7]),int(string[8:10]))
    return d


def check_errors(status):
    new_status=1
    if os.path.isfile('1_ifs2lm/job.out'):
        print('reading job.out files')
        f = open('1_ifs2lm/job.out','r')
        lines = (' ').join(f.readlines()[10:])
        f.close()
        if 'ERROR' in lines or 'error' in lines:
            new_status=-1
    if os.path.isfile('2_lm_c/job.out'):
        f = open('2_lm_c/job.out','r')
        lines = (' ').join(f.readlines()[10:])
        f.close()
        if 'ERROR' in lines or 'error' in lines:
            new_status=-1
    if os.path.isfile('3_lm2lm/job.out'):
        f = open('3_lm2lm/job.out','r')
        lines = (' ').join(f.readlines()[10:])
        f.close()
        if 'ERROR' in lines or 'error' in lines:
            new_status=-1
    if os.path.isfile('4_lm_f/job.out'):
        f = open('4_lm_f/job.out','r')
        lines = (' ').join(f.readlines()[10:])
        f.close()
        if 'ERROR' in lines or 'error' in lines:
            new_status=-1
    if new_status==-1:
        if status==-1:
            return -2
        else:
            return -1
    else: return 1
        
# =============================================================================
# Check status last run
# 0 -Not send 
# 1- Submitted
# 2- Succesful
# -1- Unsuccesful, trying with higher idbg_level
# -2- Twice unsuccesful. Stoping simualation
# =============================================================================

dataframe=pd.read_csv(name_control_dataframe,sep="\t")
for i in range(len(dataframe)):
    print (i)
    print(dataframe.loc[i])
    
    #If already succesful continue
    if dataframe['status'][i]==2:
        continue
    
    #If submited previously, check status
    if dataframe['status'][i]==1 or dataframe['status'][i]==-1:
#        new_status=1
        new_status=check_errors(dataframe['status'][i])
        if new_status>0:
            new_status=2
            #checking that the timestep is what it should be
#            dt=get_dt()
#            a=os.system("sed -i 's/ dt=%s/ dt=%1.1f/g' %s/run"%(dt,dataframe['dt'][i],main_simulation_step))
            if copy:
                print('Syncronizing files to %s'%saving_folder)
#                os.system('rsync -aq output/ %s'%saving_folder)
    
                os.system('sbatch sync_out.sh output/lm_c %s'%saving_folder)
                os.system('sbatch sync_out.sh output/lm_f %s'%saving_folder)
                os.system('sbatch sync_out.sh 2_lm_c %s'%saving_folder)
                os.system('sbatch sync_out.sh 4_lm_f %s'%saving_folder)
        print (new_status)
        dataframe['status'][i]=new_status
        dataframe['last_update'][i]=time()
        if new_status==-2:
            #os.system('mailx -s "Sandbox-Chainer: STOPPED SIMULATION AFTER STEP %s " $USER'%dataframe['start_date'][i])
            dataframe.to_csv(name_control_dataframe,mode = 'w',sep="\t", index=False)    
            print('Error detected in simulation. Exiting')
            sys.exit(1)
        if new_status==-1:
            print('Error detected in simulation (-1). Resubmiting')
            print('Multiplying idbg by 10')
            idbg=get_idbg()
            multiply_idbg()
            new_idbg=get_idbg()
            dataframe['idbg_level'][i]=new_idbg
            
#            print('Changing dt to half')
#            dt=get_dt()
#            new_dt=closer_5(dt/2)
#            if new_dt==0:
#                new_dt=2
#            a=os.system("sed -i 's/ dt=%s/ dt=%1.1f/g' %s/run"%(dt,new_dt,main_simulation_step))
#            dataframe['dt'][i]=new_dt
            #os.system('mailx -s "Sandbox-Chainer: STOPPED SIMULATION AFTER STEP %s " $USER'%dataframe['start_date'][i])
            dataframe.to_csv(name_control_dataframe,mode = 'w',sep="\t", index=False)    
#            sys.exit(1)
            break
    
    #IF not submited, submit
    if dataframe['status'][i]==0:
        d_str=create_datetime(dataframe['start_date'][i])
        dt=get_dt()
        a=os.system("sed -i 's/ dt=%s/ dt=%1.1f/g' %s/run"%(dt,dataframe['dt'][i],main_simulation_step))
        idbg=get_idbg()
        a=os.system("sed -i 's/  idbg_level = %i/  idbg_level = %i/g' %s/run"%(idbg,dataframe['idbg_level'][i],main_simulation_step))

        a=0
        a=edit_and_submit_run(d_ini,d_str,dataframe['h_str'][i],dataframe['h_end'][i])

        if a:
            dataframe['status'][i]=-5
            dataframe['last_update'][i]=time()
        else:
            new_status=1
            dataframe['status'][i]=new_status
            dataframe['last_update'][i]=time()
        dataframe.to_csv(name_control_dataframe,mode = 'w',sep="\t", index=False)    
        break        

if new_status==1 or new_status==-1:
    sys.exit(0)
else:
    sys.exit(1)

