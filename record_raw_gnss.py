import sys,os
import timep
import datetime
import psutil
import shutil #shell utilities


i = datetime.datetime.now()
input_stream = 'ttyACM0' #serial


time_min = 3  #minutes
time_sec = time_min*60
print ("Formato dd-mm-yyyy =  %s-%s-%s" % (i.day, i.month, i.year))
print ("Formato hh:mm:ss = %s:%s:%s" % (i.hour, i.minute, i.second))
out_ubx= "raw_obs_%s-%s-%s_%s:%s.ubx" % (i.day, i.month, i.year, i.hour, i.minute)
print(out_ubx)
run_str2str = "/home/pi/Lorenzo/RTKLIB/app/str2str/gcc/str2str -in serial://ttyACM0#ubx -out file:///home/pi/Lorenzo/code/record_raw_gnss/output_ubx/%s &" %(out_ubx)
print(run_str2str)

os.system(run_str2str)
a = []
time.sleep(2)
processi = filter(lambda p: p.name() == "str2str", psutil.process_iter())
for i in processi:
    a.append(i.pid)
    print (i.name, i.pid, a)


process_ID = a[-1] #if there are more str2str procces, the PID are appended in this array. The PID of the str2srt proccess launched by this script is the last element of the array.
print (process_ID)

time.sleep(time_sec)
os.system("sudo kill %s" %process_ID)



def RecordRaw():
    ''' Function to record raw GNSS data from a ublox receiver.
        The receiver configuration is not set in this script and must be set using the u-center software
        Input parameters:
        - time 
        - serial port 
        The raw GNSS data are saved in the ubx format in the folder ./output_ubx


'''
    

def RinexConverter():

    '''Function to convert a raw GNSS file from ubx format to RINEX format using CONVBIN module of rtklib

'''

def Hatanaka():
    '''Function to compress a RINEX file using the hatanaka compression format
    
'''

def main():


if __name__ == "__main__":
    main()


