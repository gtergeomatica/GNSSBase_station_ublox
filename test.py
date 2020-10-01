from ftplib import FTP
import sys,os
from credenziali import *
from datetime import datetime, timedelta
from record_raw_gnss_dev import *

''' 
server = 'localhost'
username = 'generic_user'
password = 'password'
myFTP = ftplib.FTP(server, username, password)
myPath = r'/Users/olivier/Documents/essai'

'''
def uploadThis(path):
    files = os.listdir(path)
    os.chdir(path)
    for f in files:
        if os.path.isfile(f):
            fh = open(f, 'rb')
            myFTP.storbinary('STOR %s' % f, fh)
            fh.close()
        elif os.path.isdir(f):
            myFTP.mkd(f)
            myFTP.cwd(f)
            uploadThis(f)
    myFTP.cwd('..')
    os.chdir('..')


def chdir(ftp,dir): 
    folder_name='pippo'
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


out_raw = "raw_obs_LIGE_20202741700"
nome_file='LIGE00ITA_R_20202741700_01H_01S.20O'
Stazione1=GNSSReceiver(out_raw,model='UBLOX ZED F9P',antenna="HEMISPHERE A45",rtklib_path='/home/pi/RTKLIB_demo5/',st_coord=(4509156.9882,709152.4855,4440014.3496))
print(Stazione1)

rin_file=Stazione1.RinexConverter("'LIGE'","'LIDAR ITALIA GNSS Permanent Station'",nome_file)
sys.exit()

remote_folder='/www.gter.it/stazione_gnss_ufficio/dati_rinex/'
day_of_year = datetime.utcnow().utctimetuple().tm_yday
year=datetime.utcnow().utctimetuple().tm_year
hour=datetime.utcnow().utctimetuple().tm_hour
hour_start=hour-1
months=datetime.utcnow().utctimetuple().tm_mon
days=datetime.utcnow().utctimetuple().tm_mday
minutes=datetime.utcnow().utctimetuple().tm_min
start_time='%04d%03d%02d%02d'%(year,day_of_year,hour,minutes)
giorno_locale=datetime.now().timetuple().tm_yday
ora_locale=datetime.now().timetuple().tm_hour
anno_locale=datetime.now().timetuple().tm_year
minuti_locali=datetime.now().timetuple().tm_min
print(start_time)
start_time_locale='%04d%03d%02d%02d'%(anno_locale,giorno_locale,ora_locale,minuti_locali)
print(start_time_locale)
'''
ftp = FTP(ftp_url)  
ftp.login(ftp_user, ftp_password) 
chdir(ftp,remote_folder)
ftp.quit()'''


