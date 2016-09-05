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
#/* ./CCTV-ls.sh 192.168.0.5 1                                         */
#/**********************************************************************/

if [ "$2" == "" ]
then
   echo $0 [IP_ADDRESS] [DAYS_AGO]
else
   rm ./TEMP/*.h264
   mkdir TEMP
   cp CCTV_rsa ./TEMP/
   cd TEMP

   export THISDAY=`date +%Y-%m-%d -d "$2 day ago"`

   # ../CCTV-get.sh $1 "$THISDAY"_*
   # cat "$THISDAY"_*.h264 > FULL_VIDEO_$THISDAY.h264

   echo GETTING: "$THISDAY"_2*
   ../CCTV-get.sh $1 "$THISDAY"_2*
   echo GETTING: "$THISDAY"_0*
   ../CCTV-get.sh $1 "$THISDAY"_0*
   cat "$THISDAY"_*.h264 > FULL_VIDEO_$THISDAY.h264

   # ../CCTV-get.sh $1 "$THISDAY"_00-*
   # ../CCTV-get.sh $1 "$THISDAY"_01-*
   # ../CCTV-get.sh $1 "$THISDAY"_02-*

   cd ..
fi

