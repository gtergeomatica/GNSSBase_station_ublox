# raw_data_from_ublox
This repository contains some script for automatically record raw GNSS data in ubx property format, convert them in RINEX format and compress them by Hatanaka compression format.

The script are thought for a ublox receiver plugged to a raspberry through a usb cable. Moreover the scripts have been conceived for a Linux (Debian-like) operating system.

To record raw data the free and open source rtklib sofwater is exploited. In particular the modules str2str and convbin are used, so they have to be downloaded and compiled. [Download RTKLIB here](https://github.com/tomojitakasu/RTKLIB "RTKLIB git hub repository").

The user have to specify the following inputs:
* time for data acquisition
* path to rtklib modules
* usb serial port

By running record_raw_gnss.py three file are generated and saved in the properly folders:
* raw GNSS data in ubx format, in ./output_ubx
* raw GNSS data in RINEX format in ./output_rinex
* compress RINEX file in hatanaka format in ./output_hatanaka

The name of output file contains the date of the starting moment

