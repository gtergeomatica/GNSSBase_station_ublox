# raw_data_from_ublox
This repository contains some script for automatically record raw GNSS data in ubx property format, convert them in RINEX format and compress them by Hatanaka compression format.

The script are thought for a ublox receiver plugged to a raspberry through a usb cable. Moreover the scripts have been conceived for a Linux (Debian-like) operating system.

To record raw data the free and open source rtklib sofwater is exploited. In particular the modules str2str and convbin are used, so they have to be downloaded and compiled. [Download RTKLIB here](https://github.com/tomojitakasu/RTKLIB "RTKLIB git hub repository").

If you use double frequency receivers with also Galileo constellation, the suggestion is to use the RTKLIB demo 5 version. [Download it here](https://github.com/rtklibexplorer/RTKLIB/tree/demo5).

In the record_raw_gnss_dev.py script are also implemented function to automatically upload the recorded data, in RINEX format, to a ftp server.
In order to make this function work properly a file named credenziali.py must be created in the same folder. The structure of credenziali.py is:
```python

ftp_url='ftp.myserver.com' #insert your server address
ftp_user='user' #insert your user
ftp_password='password' #insert your password

```
A function to eliminate the recorded files once uploaded is also implemented in order not to fill the raspberry storage memory

The user have to specify the following inputs:
* time for data acquisition in minutes
* path to rtklib modules
* usb serial port
* name and path to remote folder (hosted in the ftp server)

It's possible to record hourly files using this script by scheduling the script in the cron job. For example you can add the following line to the /etc/crontab file

```
0 *  * * *   pi /usr/bin/python3 /home/pi/REPOSITORY/raw_data_from_ublox/record_raw_gnss_dev.py > /tmp/record_raw_gnss.log 2>&1

```

The script generate also daily folder where hourly files are stored in a orderly way:

![Immagine1](./img/ftp-screen1.png)

![Immagine2](./img/ftp-screen2.png)

By running record_raw_gnss.py three file are generated and saved in the properly folders:
* raw GNSS data in ubx format, in ./output_ubx
* raw GNSS data in RINEX format in ./output_rinex




