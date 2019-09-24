#!/usr/bin/python

import os
import sys
import glob
import shutil
import time
import datetime
import subprocess
import pygame
import Common
import Config


ARG_EXE = 0
ARG_REGION_ID = 1
ARG_FILESPEC = 2


def ProcessFrames(BitMap, LastBitMap, ThisFile, ThisFilename):
   #   /***************************************/
   #  /* Compare only the areas scanning for */
   # /* movement in the BMP frames.         */
   #/***************************************/
   for Region in Config.REGIONS[int(sys.argv[ARG_REGION_ID])]:
      DiffCount = 0
      for y in range(Region[Config.REGION_Y_LEN]):
         for x in range(Region[Config.REGION_X_LEN]):
            if BitMap.get_at([x + Region[Config.REGION_X_OFFSET], y + Region[Config.REGION_Y_OFFSET]]) != LastBitMap.get_at([x + Region[Config.REGION_X_OFFSET], y + Region[Config.REGION_Y_OFFSET]]):
               DiffCount += 1
            x += Region[Config.REGION_STEP]
         y += Region[Config.REGION_STEP]
      #   /******************************************************/
      #  /* If the frames are differnt enough, copy the        */
      # /* current frame to the result directory and display. */
      #/******************************************************/
      DiffPercent = (10000 * DiffCount) / (Region[Config.REGION_X_LEN] * Region[Config.REGION_Y_LEN])
      if DiffPercent > Region[Config.REGION_MIN_PERCENT_DIFF] * 100:
         shutil.copyfile(ThisFile, "./DETECTED/{:s}_{:08d}.png".format(ThisFilename, Count))
         Common.DisplayBMP(ThisSurface, BitMap, int(sys.argv[ARG_REGION_ID]))



if len(sys.argv) <= ARG_FILESPEC:
   print("\n{:s} [REGION_ID] [h264_VIDEO_FILE]\n".format(sys.argv[ARG_EXE]))
   print("e.g.")
   print("\n{:s} 1 '/media/user/BONET_DENT/2019-09-03_*.h264'\n".format(sys.argv[ARG_EXE]))
   print("\n{:s} 2 '/home/user/Downloads/SMALL_FULL_VIDEO_2019-09-05.h264'\n".format(sys.argv[ARG_EXE]))
else:
   #  /***************************/
   # /* Initialise application. */
   #/***************************/
   ThisSurface = Common.Initialise()

   if os.path.isdir("DETECTED") == True:
      shutil.rmtree("DETECTED")
   os.mkdir("DETECTED")

   #  /***********************************************/
   # /* Get the list of h264 files to be processed. */
   #/***********************************************/
   FileList = glob.glob(sys.argv[ARG_FILESPEC])
   SortedFileList = sorted(FileList)
   for Filename in SortedFileList:
      #  /***********************************************************/
      # /* Get the filename only of the h264 file to process next. */
      #/***********************************************************/
      ThisFilename = Filename[Filename.rfind("/")+1:Filename.rfind(".")]

      #  /******************************************************/
      # /* Remove the temporary working files from last time. */
      #/******************************************************/
      if Config.SKIP_PROCESSING == False:
         if os.path.isdir("temp") == True:
            shutil.rmtree("temp")
         os.mkdir("temp")

      #   /*******************************************************************/
      #  /* Start pre-processing the h264 video file into BMP image frames. */
      # /* Four frames per second, scaled to 640x480 and in monochrome.    */
      #/*******************************************************************/
      LastProcess = datetime.datetime.now()
      print("{:s} - {:d} - START PROCESSING: {:s}".format(LastProcess.strftime("%Y-%m-%d %H:%M:%S"), len(SortedFileList), ThisFilename))
#      os.system("ffmpeg -i {:s} -vf 'scale=640:480,format=monow' -r 4 ./temp/{:s}_%08d.png 2>/dev/null &".format(Filename, ThisFilename))
      os.system("ffmpeg -i {:s} -vf 'scale=640:480,format=monow' -r 10 ./temp/{:s}_%08d.png 2>/dev/null &".format(Filename, ThisFilename))

      #  /********************************************************************/
      # /* Skip the first few frames to allow the video exposure to settle. */
      #/********************************************************************/
      Count = Config.SKIP_FIRST_FRAMES
      #  /********************************************************************/
      # /* Display first frame of video to indicate processing has started. */
      #/********************************************************************/
      ThisFile = "./temp/{:s}_{:08d}.png".format(ThisFilename, Count)
      NextFile = "./temp/{:s}_{:08d}.png".format(ThisFilename, Count + 1)
      ExitFlag = False
      while ExitFlag == False:
         time.sleep(0.1)
         ExitFlag = IsNextFile = os.path.isfile(NextFile)
      BitMap = pygame.image.load(ThisFile)
      Common.DisplayBMP(ThisSurface, BitMap, int(sys.argv[ARG_REGION_ID]))
      #   /******************************************/
      #  /* Process until there have been no more  */
      # /* BMP files to process for five seconds. */
      #/******************************************/
      ExitFlag = False
      while ExitFlag == False:
         #  /**********************************/
         # /* Check if next BMP file exists. */
         #/**********************************/
         ThisFile = "./temp/{:s}_{:08d}.png".format(ThisFilename, Count)
         NextFile = "./temp/{:s}_{:08d}.png".format(ThisFilename, Count + 1)
         IsNextFile = os.path.isfile(NextFile)
         if LastProcess + datetime.timedelta(seconds = 5) < datetime.datetime.now() and IsNextFile == False:
            #  /****************************/
            # /* Process final BMP frame. */
            #/****************************/
            time.sleep(1)
            LastBitMap = BitMap
            BitMap = pygame.image.load(ThisFile)
            ProcessFrames(BitMap, LastBitMap, ThisFile, ThisFilename)
            ExitFlag = True
         elif IsNextFile == True:
            LastProcess = datetime.datetime.now()
            #   /*****************************************/
            #  /* Compare the BMP of the previous frame */
            # /* to the BMP of the current frame.      */
            #/*****************************************/
            LastBitMap = BitMap
            BitMap = pygame.image.load(ThisFile)
            ProcessFrames(BitMap, LastBitMap, ThisFile, ThisFilename)
            Count += 1
         else:
            #  /********************************************/
            # /* Allow next BMP file to complete writing. */
            #/********************************************/
            time.sleep(1)

