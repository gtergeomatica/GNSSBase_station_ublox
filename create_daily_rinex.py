import sys,os
import time
from datetime import datetime, timedelta
#import psutil
#import shutil #shell utilities
import errno
from ftplib import FTP
from credenziali import *
import wget
from record_raw_gnss_dev import ftpPush, chdir, directory_exists, rinex302filename



def getFile(folder,filename):
    '''
    Function to get RINEX file from ftp folder
    
    '''
    
    try:
        obsfile=wget.download('https://{}/{}'.format(folder,filename),out='{}/rinex_temp'.format(os.path.dirname(os.path.realpath(__file__))))
        #print(type(obsfile))
    except Exception as e:
        print(e)



def ftpPush(ftp,path,infile,folder_name):
    '''
    Function to send a file to an ftp server
    '''
    #folder_name='%04d-%02d-%02d'%(datetime.utcnow().utctimetuple().tm_year,datetime.utcnow().utctimetuple().tm_mon,datetime.utcnow().utctimetuple().tm_mday)
    chdir(ftp,path,folder_name)
    try:

        with open('{}/rinex_temp/{}'.format(os.path.dirname(os.path.realpath(__file__)),infile), 'rb') as f:  
            
            ftp.storbinary('STOR {}{}/{}'.format(path,folder_name,infile), f)  
        
        return True
    except Exception as e:
        print('file non caricato sul server per la seguente ragione: {}'.format(e))
        
        return False
def rinexSplice(tipologia,cartella_remota,contenuti,ftp,anno,mese):
    '''
    funzione che implementa una serie di comandi per 
    scaricare rinex orari ad 1 sec, 
    ricampionarli a 30 sec,
    unirli in un unico file giornaliero,
    caricare il file sul server

    PER ORA LA FUNZIONE PRENDE TRE UN INPUT:
    serve per dividere file di osservabili da file navigazionali
    e le si passano anche il percorso della cartella sul server e i suoi contenuti
    IN FUTURO MEGLIO RENDERLA PIU GENERICA
    '''
    if not os.path.exists('{}/rinex_temp'.format(os.path.dirname(os.path.realpath(__file__)))):
        os.makedirs('{}/rinex_temp'.format(os.path.dirname(os.path.realpath(__file__))))
    print('\nScarico file orari in locale')
    for i in contenuti:
        if i.startswith('LIGE') and i.endswith(tipologia):
            print(i)
            getFile(cartella_remota,i)

            #stringa_nomi+='{}/rinex_temp/{} '.format(os.path.dirname(os.path.realpath(__file__)),i)
    #print(stringa_nomi)

    print(os.listdir('{}/rinex_temp'.format(os.path.dirname(os.path.realpath(__file__)))))
    if tipologia=='MO.rnx':
        print('\nRicampionamento dei file orari a 30s')
        for i in os.listdir('{}/rinex_temp'.format(os.path.dirname(os.path.realpath(__file__)))):
            
            #print('{0}/gfzrnx_lx -finp {0}/rinex_temp/{1} -fout {0}/{2}30S_MO.rnx -smp 30'.format(os.path.dirname(os.path.realpath(__file__)),i,i[:-7]))
            os.system('{0}/gfzrnx_lx -finp {0}/rinex_temp/{1} -fout {0}/rinex_temp/::RX3:: -smp 30'.format(os.path.dirname(os.path.realpath(__file__)),i))#,i[:-7]))
            os.system('rm {0}/rinex_temp/{1}'.format(os.path.dirname(os.path.realpath(__file__)),i))
    print('\nUnione dei rinex oraro in un unico rinex giornaliero')
    stringa_nomi=''
    for i in os.listdir('{}/rinex_temp'.format(os.path.dirname(os.path.realpath(__file__)))):
        #print(i)  
        stringa_nomi+='{}/rinex_temp/{} '.format(os.path.dirname(os.path.realpath(__file__)),i)  
    #print('{0}/gfzrnx_lx -finp {1}-fout {0}/rinex_temp/::RX3::'.format(os.path.dirname(os.path.realpath(__file__)),stringa_nomi))
    if tipologia=='MN.rnx':
        ieri=datetime.utcnow()-timedelta(days=1)
        nome_file_nav=rinex302filename('LIGE','%4d%3d0000'%(ieri.utctimetuple().tm_year,ieri.utctimetuple().tm_yday),1440,1,'MN',True,False)
        os.system('{0}/gfzrnx_lx -finp {1}-fout {0}/rinex_temp/{2}'.format(os.path.dirname(os.path.realpath(__file__)),stringa_nomi,nome_file_nav))
        print('\nRimozione dei file orari a 30s')

        for i in os.listdir('{}/rinex_temp'.format(os.path.dirname(os.path.realpath(__file__)))):
            #print(i[-10:-7])
            if i[-10:-7]=='01H':
                os.system('rm {}/rinex_temp/{}'.format(os.path.dirname(os.path.realpath(__file__)),i))
    elif tipologia=='MO.rnx':

        os.system('{0}/gfzrnx_lx -finp {1}-fout {0}/rinex_temp/::RX3::'.format(os.path.dirname(os.path.realpath(__file__)),stringa_nomi))
        print('\nRimozione dei file orari a 30s')
        for i in os.listdir('{}/rinex_temp'.format(os.path.dirname(os.path.realpath(__file__)))):
            #print(i[-14:-11])
            if i[-14:-11]=='01H':
                os.system('rm {}/rinex_temp/{}'.format(os.path.dirname(os.path.realpath(__file__)),i))
    
    print('\nCreo cartella annuale e mensile')
    remote_folder='/www.gter.it/stazione_gnss_ufficio/dati_rinex_giornalieri/'
    chdir(ftp,remote_folder,'{}'.format(anno))
    remote_folder+='{}/'.format(anno)
    folder_name_month='{}'.format(mese.strftime('%b'))

    #link per scaricare i navigazionali da IGS ftp://cddis.nasa.gov/gnss/data/daily/2020/brdc/

    print('\nUpload del file')
    daily_file=os.listdir('{}/rinex_temp'.format(os.path.dirname(os.path.realpath(__file__))))[0]

    if ftpPush(ftp,remote_folder,daily_file,folder_name_month)== True: #carico il file rinex registrato sul server (il caricamento avviene nel if statement)
        print('\ncancello il file sul pc')
        os.system('rm {}/rinex_temp/{}'.format(os.path.dirname(os.path.realpath(__file__)),daily_file))


def main():

    #Apro la connessione con il server
    ftp = FTP(ftp_url)  
    ftp.login(ftp_user, ftp_password) 

    day_of_year = datetime.utcnow().utctimetuple().tm_yday
    year=datetime.utcnow().utctimetuple().tm_year
    hour=datetime.utcnow().utctimetuple().tm_hour

    months=datetime.utcnow()-timedelta(days=1) #il -1 giorno serve per il caricamento dei file sul server


    # i giorni sono -1 perche' si uniscono tutti i rinex del giorno precedente
    ieri=datetime.utcnow()-timedelta(days=1)

    folder_name_day='%04d-%02d-%02d'%(ieri.utctimetuple().tm_year,ieri.utctimetuple().tm_mon,ieri.utctimetuple().tm_mday)

    print(folder_name_day)
    remote_folder='www.gter.it/stazione_gnss_ufficio/dati_rinex_orari/'
    remote_folder+='{}/{}/{}'.format(year,months.strftime('%b'),folder_name_day)

    ftp.cwd(remote_folder)
    contents = ftp.nlst()  # List CWD contents securely.
    osservabili='MO.rnx'
    navigazionali='MN.rnx'
    rinexSplice(osservabili,remote_folder,contents,ftp,year,months)
    rinexSplice(navigazionali,remote_folder,contents,ftp,year,months)

if __name__ == "__main__":
    main()


