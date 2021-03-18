#!/usr/bin/env python
# Copyleft Gter srl 2019
#Lorenzo Benvenuto


import sys,os
import time
from datetime import datetime, timedelta
from gnss_receiver import *


author = "LIGE"

######### data ############################
year=datetime.utcnow().utctimetuple().tm_year
day_of_year = datetime.utcnow().utctimetuple().tm_yday
hour=datetime.utcnow().utctimetuple().tm_hour
minutes=datetime.utcnow().utctimetuple().tm_min
months=datetime.utcnow()#-timedelta(days=1)
###############################################

remote_folder='/www.gter.it/stazione_gnss_ufficio/dati_rinex_orari/'
folder_name_day='%04d-%02d-%02d'%(datetime.utcnow().utctimetuple().tm_year,datetime.utcnow().utctimetuple().tm_mon,datetime.utcnow().utctimetuple().tm_mday)

start_time='%04d%03d%02d%02d'%(year,day_of_year,hour,minutes)
out_raw=out_raw = "raw_obs_%s_%s" % (author,start_time)
Stazione1=GNSSReceiver(out_raw,model='UBLOX ZED F9P',antenna="HEMISPHERE A45",rtklib_path='/home/pi/RTKLIB_demo5/',st_coord=(4509156.9882,709152.4855,4440014.3496))#create the isatnce: if not specified the typical characteristics of the gnss receiver are those of NARVALO BOX
print(Stazione1)
process=Stazione1.RecordRaw()
time.sleep(60) #serve aspettare nel caso in cui gli script start e stop vengono lanciati insieme (avviene nel primo avvio)
try:
    os.system('rm {}/output.txt'.format(os.path.dirname(os.path.realpath(__file__))))
except Exception as e:
    print (e)

with open('{}/output.txt'.format(os.path.dirname(os.path.realpath(__file__))), 'w') as logfile:
            logfile.write('{},{},{},{},{},{},{}'.format(process,out_raw,start_time,remote_folder,year,months.strftime('%b'),folder_name_day))
