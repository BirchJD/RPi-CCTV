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
#/* Start motion detection capture of jpg image files using the motion */
#/* Linux package.                                                     */
#/*                                                                    */
#/* Uncomment this line in the .bashrc file and ensure the other start */
#/* scripts are commented out.                                         */
#/**********************************************************************/

export ProcCount=`ps -ef | grep -c Run-Motion.sh`
echo $ProcCount

if [ $ProcCount -eq 1 ]
then
	sudo modprobe bcm2835-v4l2

	setterm -blank 0

   sleep 15

	sudo mkdir -p /DATA
	sudo mount /dev/sda /DATA
	sudo chown -R pi:users /DATA

	./Run-Motion.sh
fi

