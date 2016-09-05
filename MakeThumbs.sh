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
#/* Convert a video file into a series of frame image thumbnail files. */
#/*                                                                    */
#/* e.g.                                                               */
#/* ./MakeThumbs.sh 2016-04-15_22-22-07.h264                           */
#/**********************************************************************/

if [ "$1" == "" ]
then
   echo $0 [MEDIA_FILE]
else
   rm -r /DATA/THUMBNAILS
   mkdir /DATA/THUMBNAILS

   avconv -i /DATA/$1 -vf select="not(mod(n\,125))" '/DATA/THUMBNAILS/IMAGE_%05d.jpg'
fi

