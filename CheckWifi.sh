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
#/* Periodically check the Raspberry Pi Wifi interface is connected by */
#/* pinging the local router IP address, if it is successful do        */
#/* nothing. If pinging the router fails, reconnect to the Wifi        */
#/* network.                                                           */
#/*                                                                    */
#/* This prevents a Raspberry Pi from becoming unreachable. If an      */
#/* attempted connection fails, wait for the check period and retry    */
#/* the connection.                                                    */
#/**********************************************************************/

# crontab -e
# 0,5,10,15,20,25,30,35,40,45,50,55 * * * * /home/pi/RPi-CCTV-master/CheckWifi.sh >> /home/pi/CheckWifi.log

ping -nq -W 1 -I wlan0 -c 1 192.168.0.1 2>&1 > /dev/null

if [ $? -eq 0 ]
then
   echo Wifi Up - No Action
else
   echo Wifi Issues - Restart Network Interface

   sudo ip link set wlan0 down
   sleep 2
   sudo ip link set wlan0 up
fi

