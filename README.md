# raw_data_from_ublox
This repository contains some script for automatically record raw GNSS data in ubx property format, convert them in RINEX format and compress them by Hatanaka compression format.

The script are thought for a ublox receiver plugged to a raspberry through a usb cable. Moreover the scripts have been conceived for a Linux (Debian-like) operating system.

To record raw data the free and open source rtklib sofwater is exploited. In particular the modules str2str and convbin are used, so they have to be downloaded and compiled. [Download here](https://github.com/tomojitakasu/RTKLIB "RTKLIB git hub repository").



