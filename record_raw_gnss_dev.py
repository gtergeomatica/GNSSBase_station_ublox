#!/usr/bin/env python
# Copyleft Gter srl 2019
#Lorenzo Benvenuto


import sys,os
import time
import datetime
import psutil
import shutil #shell utilities
import errno


class GNSSReceiver:
    '''This class describes the possibile action that a generic GNSS receiver connected to a microprocessor can do'''
    
    def __init__(self, out_raw="default_filename", model="Ublox neo m8t", serial="ttyACM0", raw_format="ubx",repo_absolute_path="/home/pi/Lorenzo/code/raw_data_from_ublox/"):
        self.model=model
        self.serial=serial
        self.raw_format=raw_format
        self.out_raw=out_raw
        self.repo_absolute_path=repo_absolute_path #the path where the repository has been cloned
    
    def __str__(self):
        return "\tReceiver: %s\n\tSerial: %s\n\tGNSS raw format: %s\n\tGNSS raw data file: ./output_ubx/%s\n"%(self.model,self.serial,self.raw_format,self.out_raw)


    def RecordRaw(self,time_min):
        ''' Method to record raw GNSS data from a ublox receiver.
            The receiver configuration is not set in this script and must be set using the u-center software
            Input parameters:
            - time 
            
            The raw GNSS data are saved by default in the ubx format in the folder ./output_ubx
    '''
        #time_min = 1 #time for raw data recording
        time_sec = time_min*60
        out_file = "./output_ubx/%s.%s"%(self.out_raw,self.raw_format)
        print(out_file)    
        str2str_path="/home/pi/Lorenzo/RTKLIB/app/str2str/gcc/str2str" #path to str2str executable
        run_str2str = "%s -in serial://%s#%s -out file://%s &" %(str2str_path, self.serial, self.raw_format, out_file)
        print(run_str2str)
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

    def RinexConverter(self):

        '''Function to convert a raw GNSS file from ubx format to RINEX format using CONVBIN module of rtklib

    '''
        infile = "./output_ubx/%s.%s"%(self.out_raw,self.raw_format)
        outfile_obs = "./output_rinex/%s.obs"%(self.out_raw)
        outfile_nav = "./output_rinex/%s.nav"%(self.out_raw)
        convbin_path="/home/pi/Lorenzo/RTKLIB/app/convbin/gcc/convbin"
    
        run_convbin_obs = "%s %s -o %s -n %s"%(convbin_path, infile, outfile_obs, outfile_nav)
        print("\n************* Conversion ubx --> RINEX *************\n")
        os.system(run_convbin_obs)
        print("\n************* Done! *************\n")
            
    
    
    
    
    def Hatanaka():
        '''Function to compress a RINEX file using the hatanaka compression format
        
    '''
        pass

def main():
    print("\n***************** START SCRIPT *****************\n")
    time_min = 1  #minutes
       
    out_path = "/home/pi/Lorenzo/code/raw_data_from_ublox/output_ubx"
    now = datetime.datetime.now()
    out_raw = "raw_obs_%s-%s-%s_%s:%s" % (now.day, now.month, now.year, now.hour, now.minute)
    
    Stazione1=GNSSReceiver(out_raw) #create the isatnce: if not specified the typical characteristics of the gnss receiver are those of NARVALO BOX
    print(Stazione1)    
    
    Stazione1.RecordRaw(time_min) #specify the number of minutes for the raw data recording
    
    Stazione1.RinexConverter()
    prova = os.listdir("/home/pi/Lorenzo/code/raw_data_from_ublox/output_ubx")
    print(prova)
    '''
    
    path = "./output_ubx/paperino.ubx"
    try:
        with open(path) as f:
            # File exists
            print ("file exists")
    except IOError as e:
        # Raise the exception if it is not ENOENT (No such file or directory)
        print(e)
        if e.errno != errno.ENOENT:
            raise "Other kind of error"
    FunctionTest("ciao")
    print(output_test_param)
    '''



if __name__ == "__main__":
    main()


