#!/usr/bin/python


import os
import time
import glob
import pygame
import Common
import Config


#  /***************************/
# /* Initialise application. */
#/***************************/
ThisSurface = Common.Initialise(Config.TEXT_LINE_HEIGHT * Config.TEXT_LINE_COUNT)
TextFont = pygame.font.Font(None, Config.TEXT_LINE_HEIGHT)

#  /****************************************/
# /* Files identified as having movement. */
#/****************************************/
FileList = glob.glob(Config.FILESPEC_BMP)
SortedFileList = sorted(FileList)
FileCount = len(SortedFileList)

DisplayFileCount = 1
Speed = 10
SpeedCount = Speed
DirectionForward = True
PauseFlag = True
ExitFlag = False
while ExitFlag == False:
   time.sleep(0.01)
   #  /************************************/
   # /* Process application event queue. */
   #/************************************/
   for ThisEvent in pygame.event.get():
      #  /******************************************************************/
      # /* If ptyhon has posted a QUIT message, flag to exit applicaiton. */
      #/******************************************************************/
      if ThisEvent.type == pygame.QUIT:
         ExitFlag = True

      #  /***********************/
      # /* Handle key presses. */
      #/***********************/
      KeysPressed = pygame.key.get_pressed()
      if KeysPressed[pygame.K_ESCAPE]:
         ExitFlag = True
      elif KeysPressed[pygame.K_LEFT]:
         DirectionForward = False
      elif KeysPressed[pygame.K_RIGHT]:
         DirectionForward = True
      elif KeysPressed[pygame.K_UP]:
         Speed -= 1
         if Speed < 0:
            Speed = 0
      elif KeysPressed[pygame.K_DOWN]:
         Speed += 1
         if Speed > 20:
            Speed = 20
      elif KeysPressed[pygame.K_RETURN]:
         if PauseFlag:
            PauseFlag = False
         else:
            PauseFlag = True

   #  /******************************************************/
   # /* Throttle display updates to current speed setting. */
   #/******************************************************/
   SpeedCount -= 1
   if SpeedCount < 0:
      SpeedCount = Speed

      #  /*****************************/
      # /* Display text information. */
      #/*****************************/
      pygame.draw.rect(ThisSurface, Config.BLACK_COLOUR, (0, Config.BMP_RESOLUTION[1] - Config.TEXT_LINE_COUNT * Config.TEXT_LINE_HEIGHT, Config.BMP_RESOLUTION[0], Config.TEXT_LINE_COUNT * Config.TEXT_LINE_HEIGHT), 0)

      pygame.draw.rect(ThisSurface, Config.BAR_COLOUR, (0, Config.BMP_RESOLUTION[1] - Config.TEXT_LINE_COUNT * Config.TEXT_LINE_HEIGHT, Config.BMP_RESOLUTION[0] * DisplayFileCount / FileCount, Config.TEXT_LINE_HEIGHT), 0)
      pygame.draw.rect(ThisSurface, Config.LINE_COLOUR, (0, Config.BMP_RESOLUTION[1] - Config.TEXT_LINE_COUNT * Config.TEXT_LINE_HEIGHT, Config.BMP_RESOLUTION[0], Config.TEXT_LINE_HEIGHT), 1)

      ThisText = "{:s}".format(SortedFileList[DisplayFileCount - 1])
      Text = TextFont.render(ThisText, True, Config.TEXT_COLOUR)
      ThisSurface.blit(Text, (5, Config.BMP_RESOLUTION[1] - 2 * Config.TEXT_LINE_HEIGHT))

      if DirectionForward == True:
         Direction = ">>>"
      else:
         Direction = "<<<"
      ThisText = "DIRECTION: {:s} - SPEED: {:d} - FILE: {:d}/{:d}".format(Direction, 20 - Speed, DisplayFileCount, FileCount)
      Text = TextFont.render(ThisText, True, Config.TEXT_COLOUR)
      ThisSurface.blit(Text, (5, Config.BMP_RESOLUTION[1] - 1 * Config.TEXT_LINE_HEIGHT))

      #  /*****************************/
      # /* Display current BMP file. */
      #/*****************************/
      BitMap = pygame.image.load(SortedFileList[DisplayFileCount - 1])
      Common.DisplayBMP(ThisSurface, BitMap, 0)

      #  /***********************/
      # /* Animate BMP frames. */
      #/***********************/
      if PauseFlag == False:
         if DirectionForward == True:
            DisplayFileCount += 1
         else:
            DisplayFileCount -= 1

      if DisplayFileCount < 1:
         DisplayFileCount = 1
         PauseFlag = True
      elif DisplayFileCount > FileCount:
         DisplayFileCount = FileCount
         PauseFlag = True

