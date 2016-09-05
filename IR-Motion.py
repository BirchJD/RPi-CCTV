#!/usr/bin/python

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
#/* Python script to monitor an IR movement hardware sensor. When      */
#/* movement is detected, start recording video for a small period. If */
#/* additional movement is detected, extend the period of recording.   */
#/* Log times and dates of movement detection, start recording and end */
#/* recording events.                                                  */
#/**********************************************************************/

import os
import time
import datetime
import signal
import subprocess
import RPi.GPIO

#/*****************************/
#/* User configurable values. */
#/*****************************/
GPIO_PULSE_PINS = [ 15, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
PERIOD = 0.25
RECORD_PERIOD = 60.0
CMD_RECORD = "/home/pi/RPi-CCTV-master/Record.sh &"
CHECK_CMD_RECORD = "/home/pi/RPi-CCTV-master/CheckRecord.sh"
LOG_FILE = "/DATA/IR-Motion.log"


#  /****************************************/
# /* Raspberry Pi GPIO interrupt routine. */
#/****************************************/
def KeyPressCallback(GpioPin):
   global TriggerTimer
   global RecordFlag

#   print("GPIO: " + format(GpioPin, "00d"))

#  /**************************/
# /* Extend recording time. */
#/**************************/
   TriggerTimer = time.time()

#  /************************************************/
# /* Check if recording process is still running. */
#/************************************************/
   Check = subprocess.check_output(CHECK_CMD_RECORD)

#  /*********************************/
# /* Log movement detection event. */
#/*********************************/
   Now = datetime.datetime.now()
   LogLine = Now.strftime("%Y-%m-%d %H:%M:%S") + " IO: " + format(RPi.GPIO.input(GPIO_PULSE_PINS[0])) + " CHECK RECORDING: " + format(Check)
   print(LogLine)
   os.system("echo " + LogLine + " >> " + LOG_FILE)

#  /************************************************/
# /* If not currently recording, start recording. */
#/************************************************/
   if RecordFlag == False or int(Check) < 3:
      RecordFlag = True
      os.system(CMD_RECORD)

#  /******************************/
# /* Log start recording event. */
#/******************************/
      Now = datetime.datetime.now()
      LogLine = Now.strftime("%Y-%m-%d %H:%M:%S") + " START RECORDING"
      print(LogLine)
      os.system("echo " + LogLine + " >> " + LOG_FILE)

#  /****************************************/
# /* Play movement detection alert sound. */
#/****************************************/
      os.system("sudo ./RPiBeep 14 \"5 D 0.1 6 D 0.1 5 D 0.1 6 D 0.1 5 D 0.1 6 D 0.1 5 D 0.1 6 D 0.1 5 D 0.1 6 D 0.1 5 D 0.1 6 D 0.1 5 D 0.1 6 D 0.1 5 D 0.1 6 D 0.1 5 D 0.1\"")


#  /*******************************************/
# /* Configure Raspberry Pi GPIO interfaces. */
#/*******************************************/
def InitGPIO():
   RPi.GPIO.setwarnings(False)
   RPi.GPIO.setmode(RPi.GPIO.BCM)

   for Count in range(len(GPIO_PULSE_PINS)):
      if GPIO_PULSE_PINS[Count] != 0:
         RPi.GPIO.setup(GPIO_PULSE_PINS[Count], RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_UP)
#/***********************************************************************/
#/* Killing Raspivid currently disables edge detection for some reason. */
#/* so using polling of GPIO for now instead of interrupts.             */
#/***********************************************************************/
#         RPi.GPIO.add_event_detect(GPIO_PULSE_PINS[Count], RPi.GPIO.FALLING, callback=KeyPressCallback, bouncetime=200)



#  /***************************/
# /* Initialize application. */
#/***************************/
CheckCount = 60 / PERIOD
RecordFlag = False
TriggerTimer = time.time()
InitGPIO()

#  /**************************/
# /* Main application loop. */
#/**************************/
while True:
#  /**********/
# /* Yield. */
#/**********/
   time.sleep(PERIOD)

#   /************************************/
#  /* Check for IR movement detection. */
# /* Trigger event when detected.     */
#/************************************/
   if RPi.GPIO.input(GPIO_PULSE_PINS[0]) == 1:
      KeyPressCallback(GPIO_PULSE_PINS[0])


#   /*******************************************/
#  /* When recording and no movement detected */
# /* for a given period, stop recording.     */
#/*******************************************/
   if RecordFlag == True and time.time() - TriggerTimer > RECORD_PERIOD:
#  /*****************************/
# /* Log stop recording event. */
#/*****************************/
      Now = datetime.datetime.now()
      LogLine = Now.strftime("%Y-%m-%d %H:%M:%S") + " STOP RECORDING"
      print(LogLine)
      os.system("echo " + LogLine + " >> " + LOG_FILE)

#  /*******************************/
# /* Kill the recording process. */
#/*******************************/
      os.system("killall raspivid")
      RecordFlag = False

#  /********************************************/
# /* Periodically log a process status check. */
#/********************************************/
   CheckCount -= 1
   if CheckCount < 1:
      CheckCount = 60 / PERIOD

      Now = datetime.datetime.now()
      LogLine = Now.strftime("%Y-%m-%d %H:%M:%S") + " CHECK - IO: " + format(RPi.GPIO.input(GPIO_PULSE_PINS[0])) + " REC: " + format(RecordFlag) + " PERIOD: " + format(time.time() - TriggerTimer)
      print(LogLine)
      os.system("echo " + LogLine + " >> " + LOG_FILE)


#  /*************************************************/
# /* Close Raspberry Pi GPIO use before finishing. */
#/*************************************************/
RPi.GPIO.cleanup()

