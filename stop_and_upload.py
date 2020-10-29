#!/usr/bin/env python
# Copyleft Gter srl 2019
#Lorenzo Benvenuto


import sys,os
import time
from datetime import datetime, timedelta
import psutil
import shutil #shell utilities
import errno
from ftplib import FTP
from credenziali import *
from gnss_receiver import *



def ftpPush(ftp,path,infile,folder_name):
    '''
    Function to send a file to an ftp server
    '''
    #folder_name='%04d-%02d-%02d'%(datetime.utcnow().utctimetuple().tm_year,datetime.utcnow().utctimetuple().tm_mon,datetime.utcnow().utctimetuple().tm_mday)
    chdir(ftp,path,folder_name)
    try:

        with open('{}/output_rinex/{}'.format(os.path.dirname(os.path.realpath(__file__)),infile), 'rb') as f:  
            
            ftp.storbinary('STOR {}{}/{}'.format(path,folder_name,infile), f)  
        
        return True
    except Exception as e:
        print('file non caricato sul server per la seguente ragione: {}'.format(e))
        
        return False

def chdir(ftp,dir,folder_name): 
    '''
    Funzione per creare in automatico una cartella giornaliera per i rinex orari
    La funzione controlla che la cartella non esista già e nel caso la crea
    La funzione copia in automatico nella cartella creata i file per lo stile
    '''

    #folder_name='%04d-%02d-%02d'%(datetime.utcnow().utctimetuple().tm_year,datetime.utcnow().utctimetuple().tm_mon,datetime.utcnow().utctimetuple().tm_mday)
    if directory_exists(ftp,dir,folder_name) is False: # (or negate, whatever you prefer for readability)
        ftp.mkd(dir+folder_name)
        path_local='{}/DisplayDirectoryContents'.format(os.path.dirname(os.path.realpath(__file__)))
        path_remote='{}{}'.format(dir,folder_name)
      

        def uploadAllfiles(path_local,path_remote):
            files = os.listdir(path_local)
            for doc in files:
                print(doc)
                try:
                    print('{}/{}'.format(path_local,doc))
                    with open('{}/{}'.format(path_local,doc), 'rb') as f:
                        ftp.storbinary('STOR {}/{}'.format(path_remote,doc), f)
                except IsADirectoryError:
                    print('ciao')
                    path_local_new='{}/DisplayDirectoryContents/{}'.format(os.path.dirname(os.path.realpath(__file__)),doc)
                    print(path_local_new)
                    path_remote_new='{}/{}'.format(path_remote,doc)
                    ftp.mkd(path_remote_new)
                    uploadAllfiles(path_local_new,path_remote_new)
                except Exception as e:
                    print(e)
                    return
        uploadAllfiles(path_local,path_remote)

    else:
        return

# Check if directory exists (in current location)
def directory_exists(ftp,dir,fname):
    ftp.cwd(dir)
    filelist = []
    ftp.retrlines('LIST',filelist.append)
    for f in filelist:   
        if f.split()[-1] == fname:
            return True
    return False





def main():
    try:

        with open('{}/output.txt'.format(os.path.dirname(os.path.realpath(__file__))), 'r') as logfile:

            for line in logfile:
                currentline = line.split(",")
                pid=currentline[0]
                out_raw=currentline[1]
                start_time=currentline[2]
                remote_folder=currentline[3]
                year=currentline[4]
                months=currentline[5]
                folder_name_day=currentline[6]
    except Exception as e:
        print('non posso proseguire per il seguente problema: ',e)

    print(pid,out_raw,start_time,remote_folder,year,months,folder_name_day)
    time.sleep(55) #questo perchè lo script gira al minuto 59 di ogni ora, quindi devo aspettare ancora 60 sec prima di interrompere la registrazione
    try:
        os.system("sudo kill {}".format(pid))
    except Exception as e:
        print ('il processo str2str non puo\' essere interrotto per il seguente problema: ',e)

    Stazione1=GNSSReceiver(out_raw,model='UBLOX ZED F9P',antenna="HEMISPHERE A45",rtklib_path='/home/pi/RTKLIB_demo5/',st_coord=(4509156.9882,709152.4855,4440014.3496))#create the isatnce: if not specified the typical characteristics of the gnss receiver are those of NARVALO BOX



    nome_file_obs=rinex302filename('LIGE',start_time,60,1,'MO',True,False)
    nome_file_nav=rinex302filename('LIGE',start_time,60,1,'MN',True,False)

    print(nome_file_obs,nome_file_nav)

    rin_file=Stazione1.RinexConverter("'LIGE'","'LIDAR ITALIA GNSS Permanent Station'",nome_file_obs,nome_file_nav)



    ftp = FTP(ftp_url)  
    ftp.login(ftp_user, ftp_password) 
    
    print('\nCreo cartella annuale e mensile')
    
    chdir(ftp,remote_folder,'{}'.format(year))
    remote_folder+='{}/'.format(year)
    chdir(ftp,remote_folder,'{}'.format(months))
    remote_folder+='{}/'.format(months)




    #carico il file di osservabili
    if ftpPush(ftp,remote_folder,nome_file_obs,folder_name_day)== True: #carico il file rinex registrato sul server (il caricamento avviene nel if statement)
        print('cancello i file sul raspi')
        Stazione1.removeRinex(nome_file_obs)
        Stazione1.removeBinary()
    else:
        print('qualcosa non va...')
    
    #carico il file navigazionale
    if ftpPush(ftp,remote_folder,nome_file_nav,folder_name_day)== True: #carico il file rinex registrato sul server (il caricamento avviene nel if statement)
        print('cancello i file sul raspi')
        Stazione1.removeRinex(nome_file_nav)
        
    else:
        print('qualcosa non va...')
    ftp.quit()

if __name__ == "__main__":
    main()
