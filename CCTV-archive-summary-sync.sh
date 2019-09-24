#!/bin/bash

# 23 * * * * /home/pi/Desktop/RPi-CCTV/CCTV-archive-summary-sync.sh 192.168.0.202 > /home/pi/Desktop/RPi-CCTV/CCTV-archive-summary-sync.log

export THISDIR=$PWD
export ARCHIVEDIR=/media/pi/CCTV/ARCHIVE


if [ "$1" == "" ]
then
   echo $0 [IP_ADDRESS]
else
	sudo mkdir -p /media/pi/CCTV
	sudo mount /dev/sda /media/pi/CCTV
	sudo chown -R pi:users $ARCHIVEDIR

   mkdir $ARCHIVEDIR/$1

   echo SYNCING: "$ARCHIVEDIR/$1/SMALL_FULL_VIDEO_*"
   rsync -e "ssh -i /home/pi/.ssh/CCTV_rsa" -v --size-only pi@$1:/DATA/SUMMARY/SMALL_FULL_VIDEO_* $ARCHIVEDIR/$1/

   cd $THISDIR
fi

