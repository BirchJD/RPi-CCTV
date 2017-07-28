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
#/* Script to start recording CCTV video media files. Name the files   */
#/* based on the current date and time the recording started at.       */
#/* Provide the best parameter arguments for the video recording.      */
#/**********************************************************************/

export Filename=`date +%Y-%m-%d_%H-%M-%S`

raspivid -f -w 1024 -h 768 -t 3600000 -b 1000000 -ex night -br 55 -e -rot 0 -o /DATA/$Filename.h264

#raspivid -f -w 1024 -h 768 -t 3600000 -b 1000000 -ex nightpreview -br 55 -e -rot 0 -o /DATA/$Filename.h264
#raspivid -f -w 1920 -h 1080 -t 3600000 -b 2500000 -ex night -br 55 -e -rot 0 -o /DATA/$Filename.h264
