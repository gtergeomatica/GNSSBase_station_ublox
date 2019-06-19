#!/usr/bin/env python
# Copyleft Gter srl 2019
#Lorenzo Benvenuto


import sys,os
import time
import datetime
import psutil
import shutil #shell utilities
import errno


def RecordRaw(minutes, serial, rtklib_path):
    ''' Function to record raw GNSS data from a ublox receiver.
        The receiver configuration is not set in this script and must be set using the u-center software
        Input parameters:
        - time 
        - serial port 
        - path to rtklib module str2str (to the executable file)
        
        The raw GNSS data are saved in the ubx format in the folder ./output_ubx
'''

    time_sec = minutes*60
    out_path = "/home/pi/Lorenzo/code/raw_data_from_ublox/output_ubx"
    now = datetime.datetime.now()
    out_ubx = "raw_obs_%s-%s-%s_%s:%s.ubx" % (now.day, now.month, now.year, now.hour, now.minute)
    out_file = "%s/%s"%(out_path, out_ubx)
    print(out_file)    
    run_str2str = "%s -in serial://%s#ubx -out file://%s &" %(rtklib_path, serial, out_file)
    print(run_str2str)
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

def FunctionTest(parmeter):
        output_test_param="test_%s" %(parmeter)
        return output_test_param

def RinexConverter():

    '''Function to convert a raw GNSS file from ubx format to RINEX format using CONVBIN module of rtklib

'''
    pass
def Hatanaka():
    '''Function to compress a RINEX file using the hatanaka compression format
    
'''
    pass

def main():
    print("***************** START SCRIPT *****************")
    time_min = 1  #minutes
    
    #print ("Format dd-mm-yyyy =  %s-%s-%s" % (i.day, i.month, i.year))
    #print ("Format hh:mm:ss = %s:%s:%s" % (i.hour, i.minute, i.second))
    
    str2str_path="/home/pi/Lorenzo/RTKLIB/app/str2str/gcc/str2str"  #probably relative paths are better (think about changing absolute paths)
    usbSerial = "ttyACM0" #you can find it in /dev/
    #RecordRaw(time_min, usbSerial, str2str_path )

    
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
    



if __name__ == "__main__":
    main()


