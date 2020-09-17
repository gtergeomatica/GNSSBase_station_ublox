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


class GNSSReceiver:
    '''This class describes the possibile action that a generic GNSS receiver connected to a microprocessor can do'''
    
    def __init__(self, out_raw="default_filename", model="Ublox neo m8t", antenna="patch", serial="ttyACM0", raw_format="ubx",repo_absolute_path="/home/pi/REPOSITORY/raw_data_from_ublox/",rtklib_path='/home/pi/RTKLIB/'):
        self.model=model
        self.antenna=antenna
        self.serial=serial
        self.raw_format=raw_format
        self.out_raw=out_raw
        self.repo_absolute_path=repo_absolute_path #the path where the repository has been cloned
        self.rtklib_path=rtklib_path

    def __str__(self):
        return "\tReceiver: %s\n\tAntenna: %s\n\tSerial: %s\n\tGNSS raw format: %s\n\tGNSS raw data file: ./output_ubx/%s\n\trtklib path: %s\n"%(self.model,self.antenna,self.serial,self.raw_format,self.out_raw,self.rtklib_path)


    def RecordRaw(self,time_min):
        ''' Method to record raw GNSS data from a ublox receiver.
            The receiver configuration is not set in this script and must be set using the u-center software
            Input parameters:
            - time 
            
            The raw GNSS data are saved by default in the ubx format in the folder ./output_ubx
    '''
        #time_min = 1 #time for raw data recording
        time_sec = time_min*60
        out_file = "%s/output_ubx/%s.%s"%(os.path.dirname(os.path.realpath(__file__)),self.out_raw,self.raw_format)
        print(out_file)    
        str2str_path="%sapp/str2str/gcc/str2str"%(self.rtklib_path) #path to str2str executable
        run_str2str = "%s -in serial://%s#%s -out file://%s &" %(str2str_path, self.serial, self.raw_format, out_file)
        print(run_str2str)
        os.system("sudo killall str2str")   #non sicuro che sia la cosa giusta da fare
        print("\n************* Start data acquisition *************\n")
        os.system(run_str2str)
        
        a = []
        time.sleep(2)
        process = filter(lambda p: p.name() == "str2str", psutil.process_iter())
        for i in process:
            a.append(i.pid)
            print (i.name, i.pid, a)


        process_ID = a[-1] #if there are more str2str procces, the PID are appended in this array. The PID of the str2srt proccess launched by this script is the last element of the array.
        print (process_ID)

        time.sleep(time_sec)
        os.system("sudo kill %s" %process_ID)
        print("\n************* Stop data acquisition *************\n")
        return out_file

    def FunctionTest(parmeter):
            output_test_param="test_%s" %(parmeter)
            return output_test_param

    def RinexConverter(self,marker,comment,rinex_name):

        '''Function to convert a raw GNSS file from ubx format to RINEX format using CONVBIN module of rtklib

    '''
        infile = "%s/output_ubx/%s.%s"%(os.path.dirname(os.path.realpath(__file__)),self.out_raw,self.raw_format)
        outfile_obs = "%s/output_rinex/%s"%(os.path.dirname(os.path.realpath(__file__)),rinex_name)
        outfile_nav = "%s/output_rinex/%s.nav"%(os.path.dirname(os.path.realpath(__file__)),self.out_raw)
        convbin_path="%sapp/convbin/gcc/convbin"%(self.rtklib_path)
        #marker = "'LIGE'"
        #comment = "'LIDAR ITALIA GNSS Permanent Station'"
        #receiver = "'Ublox ZED F9P'"
        #antenna = "'HEMISPHERE A45'"
    
        run_convbin_obs = "%s %s -o %s -n %s -od -os -hc %s -hm %s -hr '%s' -ha '%s' -v 3.02"%(convbin_path, infile, outfile_obs, outfile_nav, comment, marker, self.model, self.antenna)
        print(run_convbin_obs)
        print("\n************* Conversion ubx --> RINEX *************\n")
        os.system(run_convbin_obs)
        print("\n************* Done! *************\n")
        return(outfile_obs)

    def removeRinex(self, filename):
        try:
            os.system('rm {}/output_rinex/{}'.format(os.path.dirname(os.path.realpath(__file__)),filename))
            return True
        except Exception as e:
            print(e)
            return False
    
    def removeBinary(self):
        try:
            os.system('rm {}/output_ubx/{}.{}'.format(os.path.dirname(os.path.realpath(__file__)),self.out_raw,self.raw_format))
            return True
        except Exception as e:
            print(e)
            return False
    
    
    
    
    def Hatanaka():
        '''Function to compress a RINEX file using the hatanaka compression format
        
    '''
        pass



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



def rinex302filename(st_code,ST,session_interval,obs_freq,data_type,data_type_flag,bin_flag,data_format='RINEX',compression=None):
    '''function to dynamically define the filename in rinex 3.02 format)
    Needed parameters
    1: STATION/PROJECT NAME (SPN); format XXXXMRCCC
        XXXX: station code
        M: monument or marker number (0-9)
        R: receiver number (0-9)
        CCC:  ISO Country CODE see ISO 3166-1 alpha-3 
    
    2: DATA SOURCE (DS)
        R – From Receiver data using vendor or other software
        S – From data Stream (RTCM or other)
        U – Unknown (1 character)
    
    3: START TIME (ST); fomrat YYYYDDDHHMM (UTC)
        YYYY - Gregorian year 4 digits,
        DDD  – day of year,
        HHMM - Hour and minutes of day
    4: FILE PERIOD (FP): format DDU
        DD – file period 
        U – units of file period.
        Examples:
        15M – 15 Minutes 
        01H – 1 Hour
        01D – 1 Day
        01Y – 1 Year 
        00U - Unspecified
    
    5: DATA FREQ (DF); format DDU
        DD – data frequency 
        U – units of data rate 
        Examples:
        XXS – Seconds,
        XXM – Minutes,
        XXH – Hours,
        XXD – Days
        XXU – Unspecified
    6: DATA TYPE (DT); format DD (default value are MO for obs and MN for nav)
        GO - GPS Obs.,
        RO - GLONASS Obs., 
        EO - Galileo Obs. 
        JO - QZSS Obs., 
        CO - BDS Obs., 
        IO – IRNSS Obs., 
        SO - SBAS Obs., 
        MO Mixed Obs., 
        GN - Nav. GPS, 
        RN- Glonass Nav., 
        EN- Galileo Nav., 
        JN- QZSS Nav., 
        CN- BDS Nav., 
        IN – IRNSS Nav., 
        SN- SBAS Nav., 
        MN- Nav. All GNSS Constellations 
        MM-Meteorological Observation 
        Etc
    7: FORMAT
        Three character indicating the data format:
        RINEX - rnx, 
        Hatanaka Compressed RINEX – crx, 
        ETC
    
    8: COMPRESSION
        .zip
        .gz
        .tar.gz
        etc
        if None the filename will ends with .YYO
    '''
    filename=''

    # STATION/PROJECT NAME

    M=0 #da capire
    R=0 #da capire

    if st_code=='SAOR':
        CCC='FRA'
    else:
        CCC='ITA'
    
    SPN='{}{}{}{}_'.format(st_code,M,R,CCC)

    filename+=SPN

    # DATA SOURCE 
    DS='R'
    filename+='{}_'.format(DS)

    # START TIME
    filename+='{}_'.format(ST)
    

    # FILE PERIOD
    interval=timedelta(seconds=session_interval*60)

    if interval.days != 0 and interval.seconds//3600 ==0:
        FP='%02dD'%(interval.days)
    elif interval.days == 0 and interval.seconds//3600 !=0:
        FP='%02dH'%(interval.seconds//3600)
    else:
        FP='00U'

    filename+='{}_'.format(FP)

    # DATA FREQ
    
    freq=timedelta(seconds=obs_freq)
    #print(freq)
    #print((freq.seconds//60)%60,freq.seconds)
    if freq.seconds!=0 and (freq.seconds//60)%60==0:
        DF='%02dS'%(freq.seconds)
    elif freq.seconds==0 and (freq.seconds//60)%60!=0:
        DF='%02dM'%((freq.seconds//60)%60)
    else:
        DF='00U'

    filename+='{}'.format(DF)

    # DATA TYPE
    if data_type_flag:
        filename+='{}_'.format(data_type)
        #parte per compressione
    else:
        if bin_flag:
            filename+='.dat'
        else:
            if compression != None:
                filename+='_{}.{}'.format(data_format,compression)      
            else:
                filename+='.{}O'.format(ST[2:4])
            
    
    return filename




def main():
    print("\n***************** START SCRIPT *****************\n")
    time_min = 60  #minutes
    
    out_path = "/home/pi/gnss_obs/stazione_gnss_ufficio"
    #now = datetime.datetime.now()
    author = "LIGE"
    
    
    
    remote_folder='/www.gter.it/stazione_gnss_ufficio/dati_rinex/'

    day_of_year = datetime.utcnow().utctimetuple().tm_yday
    year=datetime.utcnow().utctimetuple().tm_year
    hour=datetime.utcnow().utctimetuple().tm_hour
    hour_start=hour-1
    months=datetime.utcnow().utctimetuple().tm_mon
    days=datetime.utcnow().utctimetuple().tm_mday
    minutes=datetime.utcnow().utctimetuple().tm_min
    start_time='%04d%03d%02d%02d'%(year,day_of_year,hour,minutes)
    out_raw = "raw_obs_%s_%s" % (author,start_time)
    nome_file=rinex302filename('LIGE',start_time,60,1,'MO',False,False)
    

    Stazione1=GNSSReceiver(out_raw,model='UBLOX ZED F9P',antenna="HEMISPHERE A45",rtklib_path='/home/pi/RTKLIB_demo5/')#create the isatnce: if not specified the typical characteristics of the gnss receiver are those of NARVALO BOX
    print(Stazione1)    
    
    Stazione1.RecordRaw(time_min) #specify the number of minutes for the raw data recording
    
    rin_file=Stazione1.RinexConverter("'LIGE'","'LIDAR ITALIA GNSS Permanent Station'",nome)
    print(rin_file)
    
    
    ftp = FTP(ftp_url)  
    ftp.login(ftp_user, ftp_password) 
    folder_name_day='%04d-%02d-%02d'%(datetime.utcnow().utctimetuple().tm_year,datetime.utcnow().utctimetuple().tm_mon,datetime.utcnow().utctimetuple().tm_mday)
    if ftpPush(ftp,remote_folder,nome_file,folder_name_day)== True: #carico il file rinex registrato sul server (il caricamento avviene nel if statement)
        print('cancello i file sul raspi')
        Stazione1.removeRinex(nome)
        Stazione1.removeBinary()
    else:
        print('qualcosa non va...')
    ftp.quit()
if __name__ == "__main__":
    main()


