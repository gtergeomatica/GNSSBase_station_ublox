import sys,os
import time
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


process_ID = a[-1] #se ci sono piu processi rtkrcv attivi, i PID vengono messi tutti in questo array; il processo di cu mi interessa sapere il PID (perche' e' il processo rtkrcv che sto lanciando in questo momento) e' l'ultimo elemento di questo array.
print (process_ID)

time.sleep(time_sec)
os.system("sudo kill %s" %process_ID)
