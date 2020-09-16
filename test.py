from ftplib import FTP
import sys,os
from credenziali import *
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

remote_folder='/www.gter.it/stazione_gnss_ufficio/dati_rinex/'


ftp = FTP(ftp_url)  
ftp.login(ftp_user, ftp_password) 
chdir(ftp,remote_folder)
ftp.quit()
