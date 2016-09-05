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
#/* Retrieve a CCTV media file or files from a remote Raspberry Pi.    */
#/*                                                                    */
#/* e.g.                                                               */
#/* ./CCTV-get.sh 192.168.0.5 2016-08-17_20-13-10.h264                 */
#/* ./CCTV-get.sh 192.168.0.5 2016-08-17_*                             */
#/**********************************************************************/

if [ "$2" == "" ]
then
   echo $0 [IP_ADDRESS] [FILE_SPEC]
else
   scp -i CCTV_rsa "pi@$1:/DATA/$2" .
fi

