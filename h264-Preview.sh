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
#/* Then remove sets of intermediate frames from the image thumbnails  */
#/* and convert the remaining frame files back into a video to create  */
#/* a time lapse video which will be quicker to review.                */  
#/*                                                                    */
#/* e.g.                                                               */
#/* ./MakeThumbs.sh 2016-04-15_22-22-07.h264                           */
#/**********************************************************************/

# find . -name '*.h264' -exec ./h264-Preview.sh {} \;

rm -rf TEMP-FRAMES
mkdir TEMP-FRAMES

avconv -i $1 -s 320x240 -q:v 15 TEMP-FRAMES/%d.jpg

export Count=1
export Target=1
export Test=1
while [ -e "TEMP-FRAMES/$Count.jpg" ]
do
   if [ $Test -eq 30 ]
   then
      export Test=1

      mv TEMP-FRAMES/$Count.jpg TEMP-FRAMES/$Target.jpg

      Target=$((Target+1))
   else
      rm TEMP-FRAMES/$Count.jpg
   fi

   Count=$((Count+1))
   Test=$((Test+1))
done

avconv -i TEMP-FRAMES/%d.jpg $1.avi

