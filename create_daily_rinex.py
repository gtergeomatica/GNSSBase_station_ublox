import sys,os
import time
from datetime import datetime, timedelta
#import psutil
#import shutil #shell utilities
import errno
from ftplib import FTP
from credenziali import *
import wget



def getFile(folder,filename):
    '''
    Function to get RINEX file from ftp folder
    
    '''
    
    try:
        obsfile=wget.download('https://{}/{}'.format(folder,filename),out='{}/rinex_temp'.format(os.path.dirname(os.path.realpath(__file__))))
        print(type(obsfile))
    except Exception as e:
        print(e)



ftp = FTP(ftp_url)  
ftp.login(ftp_user, ftp_password) 


day_of_year = datetime.utcnow().utctimetuple().tm_yday
year=datetime.utcnow().utctimetuple().tm_year
hour=datetime.utcnow().utctimetuple().tm_hour
hour_start=hour-1
months=datetime.utcnow().utctimetuple().tm_mon
days=datetime.utcnow().utctimetuple().tm_mday
minutes=datetime.utcnow().utctimetuple().tm_min

# i giorni sono -1 perche' si uniscono tutti i rinex del giorno precedente
folder_name_day='%04d-%02d-%02d'%(datetime.utcnow().utctimetuple().tm_year,datetime.utcnow().utctimetuple().tm_mon,datetime.utcnow().utctimetuple().tm_mday-1)

print(folder_name_day)
remote_folder='www.gter.it/stazione_gnss_ufficio/dati_rinex/{}'.format(folder_name_day)


ftp.cwd(remote_folder)
contents = ftp.nlst()  # List CWD contents securely.

if not os.path.exists('{}/rinex_temp'.format(os.path.dirname(os.path.realpath(__file__)))):
    os.makedirs('{}/rinex_temp'.format(os.path.dirname(os.path.realpath(__file__))))
print('\nScarico file orari in locale')
for i in contents:
    if i.startswith('LIGE'):
        print(i)
        getFile(remote_folder,i)

        #stringa_nomi+='{}/rinex_temp/{} '.format(os.path.dirname(os.path.realpath(__file__)),i)
#print(stringa_nomi)

print(os.listdir('{}/rinex_temp'.format(os.path.dirname(os.path.realpath(__file__)))))

print('\nRicampionamento dei file orari a 30s')
for i in os.listdir('{}/rinex_temp'.format(os.path.dirname(os.path.realpath(__file__)))):
    
    #print('{0}/gfzrnx_lx -finp {0}/rinex_temp/{1} -fout {0}/{2}30S_MO.rnx -smp 30'.format(os.path.dirname(os.path.realpath(__file__)),i,i[:-7]))
    os.system('{0}/gfzrnx_lx -finp {0}/rinex_temp/{1} -fout {0}/rinex_temp/{2}30S_MO.rnx -smp 30'.format(os.path.dirname(os.path.realpath(__file__)),i,i[:-7]))
    os.system('rm {0}/rinex_temp/{1}'.format(os.path.dirname(os.path.realpath(__file__)),i))
print('\nUnione dei rinex oraro in un unico rinex giornaliero')
stringa_nomi=''
for i in os.listdir('{}/rinex_temp'.format(os.path.dirname(os.path.realpath(__file__)))):
    #print(i)  
    stringa_nomi+='{}/rinex_temp/{} '.format(os.path.dirname(os.path.realpath(__file__)),i)  
#print('{0}/gfzrnx_lx -finp {1}-fout {0}/rinex_temp/rinex_merge.20O'.format(os.path.dirname(os.path.realpath(__file__)),stringa_nomi))
os.system('{0}/gfzrnx_lx -finp {1}-fout {0}/rinex_temp/::RX3::'.format(os.path.dirname(os.path.realpath(__file__)),stringa_nomi))
print('\nRimozione dei file orari a 30s')
for i in os.listdir('{}/rinex_temp'.format(os.path.dirname(os.path.realpath(__file__)))):
    if i[-15:-10]=='_01H_':
        os.system('rm {}/rinex_temp/{}'.format(os.path.dirname(os.path.realpath(__file__)),i))
