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
#/* Extract a single jpg image from the end of the current video file  */
#/* recording. Place the file into the web server directory so it can  */
#/* be remotely viewed using a web browser.                            */
#/*                                                                    */
#/* Additionally copy the most recent log entries into the web server  */
#/* directory so they can be viewed remotely using a web browser.      */
#/**********************************************************************/

# Find the current image file and use that in case video is not in use.
export CurrentImageFile=`ls -1t /DATA/*.jpg | head -1`
if [ -f $CurrentVideoFile ]
then
   cp $CurrentVideoFile /var/www/html/image.jpg
fi

# Find the current video file.
export CurrentVideoFile=`ls -1t /DATA/*.h264 | head -1`

if [ -f $CurrentVideoFile ]
then
   # Get the header from the current video file.
   head -c $(( 1*128 )) $CurrentVideoFile > /var/www/html/temp/temp.h264

   # Get the most recent data from the current video file.
   # NOTE: If this may need to be increased for high resolution video data.
   tail -c $(( 512*1024 )) $CurrentVideoFile >> /var/www/html/temp/temp.h264

   # Get a thumbnail a couple of seconds into the most recent video data.
   avconv -i /var/www/html/temp/temp.h264 -vf select="eq(n\,60)" -vframes 1 '/var/www/html/image.jpg'
fi

# Get most recent log events.
tail -200l /DATA/IR-Motion.log > /var/www/html/log.inc

