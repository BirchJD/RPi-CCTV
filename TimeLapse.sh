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
#/* V1.00   2016-09-09  Jason Birch                                    */
#/*                                                                    */
#/* Create time lapse video from downloaded images.                    */
#/*                                                                    */
#/* e.g.                                                               */
#/* ./TimeLapse.sh 2016-09-09 1                                        */
#/**********************************************************************/

if [ "$2" == "" ]
then
   echo "$0 [DATE] [FIRST_IMAGE_NUMBER]"
else
   cd TEMP

   export FromCount=$2
   export ToCount=1
   export Error=0
   while [ $Error -le 100 ]
   do
      export From=$1_`printf "%6.6u" $FromCount`.jpg
      export To=`printf "%6.6u" $ToCount`.jpg

      if [ -f "$From" ]
      then
         if [ $FromCount -ne $ToCount ]
         then
            mv $From $To
            echo "$From => $To"
         fi
         export ToCount=$((ToCount+1))
         export Error=0
      else
         export Error=$((Error+1))
      fi
      export FromCount=$((FromCount+1))
   done

   avconv -y -r 10 -i %06d.jpg -r 10 -vcodec libx264 -crf 20 -g 15 timelapse.mp4
fi

