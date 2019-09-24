#!/usr/bin/python

# RPiCCTV - CCTV System for Raspberry Pi
# Copyright (C) 2019 Jason Birch
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

#/*************************************************************************/
#/* V1.00   2019-09-10  Jason Birch                                       */
#/*                                                                       */
#/* Scrip to make a compat summary video of the entire day for archiving. */
#/*************************************************************************/

# 30 * * * * /home/pi/RPi-CCTV-master/MakeSummary.sh > /home/pi/MakeSummary.log

import os
import sys
import glob
import time
import datetime

if os.path.isdir("/DATA/SUMMARY/") == False:
   os.mkdir("/DATA/SUMMARY/")

for DaysAge in range(1, 8):
   Now = datetime.datetime.now() - datetime.timedelta(days = 8 - DaysAge)
   FileSpec = "/DATA/{:s}".format(Now.strftime("%Y-%m-%d_*.h264"))
   ThisSummaryFilename = "/DATA/SUMMARY/{:s}".format(Now.strftime("SMALL_FULL_VIDEO_%Y-%m-%d.h264"))
   if os.path.isfile(ThisSummaryFilename) == False:
      print("PROCESSING: {:s}".format(ThisSummaryFilename))
      FileList = glob.glob(FileSpec)
      SortedFileList = sorted(FileList)
      for Filename in SortedFileList:
         ThisFilename = Filename[Filename.rfind("/")+1:Filename.rfind(".")]
         os.system("avconv -i {:s} -y -vf 'select=not(mod(n\,10)),scale=1024:768:flags=neighbor' -b:v 256k /DATA/SUMMARY/{:s}_SMALL.h264".format(Filename, ThisFilename))
         os.system("cat /DATA/SUMMARY/{:s}_SMALL.h264 >> {:s}".format(ThisFilename, ThisSummaryFilename))

      time.sleep(60)
      for Filename in SortedFileList:
         ThisFilename = Filename[Filename.rfind("/")+1:Filename.rfind(".")]
         os.remove("/DATA/SUMMARY/{:s}_SMALL.h264".format(ThisFilename))

Now = datetime.datetime.now() - datetime.timedelta(days = 8)
OldSummaryFilename = "/DATA/SUMMARY/{:s}".format(Now.strftime("SMALL_FULL_VIDEO_%Y-%m-%d.h264"))
os.remove(OldSummaryFilename)

