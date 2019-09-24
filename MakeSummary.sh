#!/bin/bash

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

export ProcCount=`ps -ef | grep -c MakeSummary.py`
echo $ProcCount

if [ $ProcCount -eq 1 ]
then
   cd ~/RPi-CCTV-master/
   ./MakeSummary.py
fi

