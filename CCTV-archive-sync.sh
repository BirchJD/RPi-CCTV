#!/bin/bash

# RPiCCTV - CCTV System for Raspberry Pi
# Copyright (C) 2016 Jason Birch
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see &lt;http://www.gnu.org/licenses/>.

#/**********************************************************************/
#/* V1.00   2016-09-02  Jason Birch                                    */
#/*                                                                    */
#/* Retrieve a set of media files for a specific day, from a remote    */
#/* Raspberry Pi for the period of night time, at the specified number */
#/* of days old.                                                       */
#/*                                                                    */
#/* e.g.                                                               */
#/* ./CCTV-archive-sync.sh 192.168.0.5 1                               */
#/**********************************************************************/


export THISDIR=$PWD
export ARCHIVEDIR=/media/pi/CCTV/ARCHIVE


if [ "$2" == "" ]
then
   echo $0 [IP_ADDRESS] [DAYS_AGO]
else
   mkdir $ARCHIVEDIR/TEMP
   find $ARCHIVEDIR/TEMP/*.h264 -mtime +3 -exec rm {} \;
   cp CCTV_rsa $ARCHIVEDIR/TEMP/
   cd $ARCHIVEDIR/TEMP

#  /******************************************************************/
# /* Get the required specification of video for the specified day. */
#/******************************************************************/
   export THISDAY=`date +%Y-%m-%d -d "$2 day ago"`

   echo SYNCING: "$THISDAY"_*
   # rsync -e "ssh -i CCTV_rsa" -v --size-only --bwlimit 1600 pi@$1:/DATA/"$THISDAY"_* $ARCHIVEDIR/TEMP/
   rsync -e "ssh -i CCTV_rsa" -v --size-only pi@$1:/DATA/"$THISDAY"_* $ARCHIVEDIR/TEMP/


   cd $THISDIR
fi

