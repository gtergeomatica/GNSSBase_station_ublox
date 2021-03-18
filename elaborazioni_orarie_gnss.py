import sys,os
import time
from datetime import datetime, timedelta
import psutil
import shutil #shell utilities
import errno
from ftplib import FTP
import GNSS_liguria_download
import record_raw_gnss_dev
import wget
import sqlite3

def createTable(dbname,table):
    
    conn = sqlite3.connect('{}'.format(dbname))
    cur = conn.cursor()
    dropTableStatement = "DROP TABLE IF EXISTS {}".format(table)
    cur.execute(dropTableStatement)
    cur.execute('CREATE TABLE {} (GPST DATE PRIMARY KEY, EAST FLOAT, NORTH FLOAT, HEIGHT FLOAT, \
                 Quality_fixing INT, Satellite_number INT, SDE FLOAT, SDN FLOAT, SDU FLOAT,\
                 SDEN FLOAT,  SDNU FLOAT, SDUE FLOAT, AGE FLOAT, RATIO FLOAT)'.format(table))
    conn.commit()

    conn.close()
        
def hour2letter(ora):
    if ora ==0:
        lettera='a'
    elif ora==1:
        lettera='b'
    elif ora==2:
        lettera='c'
    elif ora==3:
        lettera='d'
    elif ora==4:
        lettera='e'
    elif ora==5:
        lettera='f'
    elif ora==6:
        lettera='g'
    elif ora==7:
        lettera='h'
    elif ora==8:
        lettera='i'
    elif ora==9:
        lettera='j'
    elif ora==10:
        lettera='k'
    elif ora==11:
        lettera='l'
    elif ora==12:
        lettera='m'
    elif ora==13:
        lettera='n'
    elif ora==14:
        lettera='o'
    elif ora==15:
        lettera='p'
    elif ora==16:
        lettera='q'
    elif ora==17:
        lettera='r'
    elif ora==18:
        lettera='s'
    elif ora==19:
        lettera='t'
    elif ora==20:
        lettera='u'
    elif ora==21:
        lettera='v'
    elif ora==22:
        lettera='w'
    elif ora==23:
        lettera='x'
    else:
        return
    return lettera
    pass

#createTable('LIGE_GNSS.db','elab_orarie')
#sys.exit()
#define time for elaboration
istante=datetime.utcnow() - timedelta(hours=1)

#istante=datetime(2021,3,int('{}'.format(sys.argv[1])),int('{}'.format(sys.argv[2])))
#istante=datetime.strptime(sys.argv[1],'%Y-%m-%d_%H')

year=istante.utctimetuple().tm_year
day_of_year = istante.utctimetuple().tm_yday 
day=istante.utctimetuple().tm_mday
hour=istante.utctimetuple().tm_hour
#print(hour)
mese=istante.utctimetuple().tm_mon
#minutes=datetime.utcnow().utctimetuple().tm_min

start_time='%04d%03d%02d00'%(year,day_of_year,hour)


#download rover observation data

nome_file_rover=record_raw_gnss_dev.rinex302filename('LIGE',start_time,60,1,'MO',True,False)
out='{}/temporary'.format(os.path.dirname(os.path.realpath(__file__)))
print(out)
link='https://www.gter.it/stazione_gnss_ufficio/dati_rinex_orari/{}/{}/{:04d}-{:02d}-{:02d}/{}'.format(year,istante.strftime('%b'),year,mese,day,nome_file_rover)
print(link)

GNSS_liguria_download.download(link,out)

#download base observation and navigation data
data_tbd=f'{istante.year:04}/{istante.month:02}/{istante.day:02}'

file_base=GNSS_liguria_download.GNSS_download('genu',data_tbd,1,hour2letter(hour),['obs','nav','gnav'],out)
obs,nav,gnav=GNSS_liguria_download.uncompress('{}/'.format(out),file_base)

obsbase_hatanaka=file_base[0][0][:-2]
navbase=file_base[1][0][:-2]
gnavbase=file_base[2][0][:-2]

#elaboration

crx2rnx='{}/CRX2RNX'.format(os.path.dirname(os.path.realpath(__file__)))

os.system('{0}/CRX2RNX {0}/temporary/{1}'.format(os.path.dirname(os.path.realpath(__file__)),obsbase_hatanaka))

obsbase=[i for i in os.listdir(out) if i.endswith('o')][0] #rivedere condizione endswith (deve risultare una lista di un solo elemento)

os.remove('{}/temporary/{}'.format(os.path.dirname(os.path.realpath(__file__)),obsbase_hatanaka))

rnx2rtkp_path='/home/ubuntu/RTKLIB_official/app/rnx2rtkp/gcc/'#'/home/ubuntu/RTKLIB_demo5_b34/app/consapp/rnx2rtkp/gcc/'

conf_file='{}/elab_lige_gps.conf'.format(os.path.dirname(os.path.realpath(__file__)))
outfile='{}/elaboration.txt'.format(out)
#rnx2rtkp_syntax -k conf_file.conf -o solution_file rover base nav
rnx2rtkp_syntax='{0}rnx2rtkp -k {1} -o {2} {3}/{4} {3}/{5} {3}/{6} {3}/{7}'.format(rnx2rtkp_path,conf_file,outfile,out,nome_file_rover,obsbase,navbase,gnavbase)
print(rnx2rtkp_syntax)
os.system(rnx2rtkp_syntax)


GENU=(496761.632,4916599.369,127.418) # E,N,H_ell ETRF2000,2008.0 UTM 32N

with open ('{}/elaboration.txt'.format(out),'r') as resultfile:
    testo=resultfile.readlines()


print(testo[-1].strip().split())
#print(os.path.dirname(os.path.realpath(__file__)))
tempo=testo[-1].strip().split()[0]
orario=testo[-1].strip().split()[1]
print(orario[0:2],orario[3:5],orario[6:11])

tempo=datetime(int(tempo[0:4]),int(tempo[5:7]),int(tempo[8:10]),int(orario[0:2]),int(orario[3:5]))

east=float(GENU[0])+float(testo[-1].strip().split()[2])
north=float(GENU[1])+float(testo[-1].strip().split()[3])
height=float(GENU[2])+float(testo[-1].strip().split()[4])
qf=testo[-1].strip().split()[5]
nsat=testo[-1].strip().split()[6]
sde=testo[-1].strip().split()[7]
snd=testo[-1].strip().split()[8]
sdu=testo[-1].strip().split()[9]
sden=testo[-1].strip().split()[10]
sdnu=testo[-1].strip().split()[11]
sdue=testo[-1].strip().split()[12]
age=testo[-1].strip().split()[13]
ratio=testo[-1].strip().split()[14]
#print(tempo, east,north,height)

#upload coordinates to a db
dbname='LIGE_GNSS.db'
tabella='elab_orarie'
conn=sqlite3.connect('{}/{}'.format(os.path.dirname(os.path.realpath(__file__)),dbname))
cur = conn.cursor()
insert_query="INSERT INTO {} VALUES ('{}',{},{},{},{},{},{},{},{},{},{},{},{},{})".format(tabella,tempo,east,north,height,qf,nsat,sde,snd,sdu,sden,sdnu,sdue,age,ratio)
try:
    cur.execute(insert_query)
except Exception as e:
    print(e)
cur.close()
conn.commit()
conn.close()

for i in os.listdir(out):
    os.remove('{}/{}'.format(out,i))
