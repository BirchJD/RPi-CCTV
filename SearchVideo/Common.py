import os
import pygame
import Config



#/***************************/
#/* Initialise application. */
#/***************************/
def Initialise(AddedTextLineHeight = 0):
   pygame.init()
   Resolution = Config.BMP_RESOLUTION
   Resolution[1] += AddedTextLineHeight
   ThisSurface = pygame.display.set_mode(Resolution, pygame.HWSURFACE | pygame.DOUBLEBUF)
   ThisVideoInfo = pygame.display.Info()

   #   /**********************************************/
   #  /* Ensure the directory to place the target   */
   # /* files where movement was detected, exists. */
   #/**********************************************/
   if os.path.isdir("DETECTED") == False:
      os.mkdir("DETECTED")

   return ThisSurface



#/***************************************************/
#/* Display a BMP file in the application window.   */
#/* Highlight the areas being scanned for movement. */
#/***************************************************/
def DisplayBMP(ThisSurface, ThisBitMap, RegionID):
   for Region in Config.REGIONS[RegionID]:
      for y in range(Region[Config.REGION_Y_LEN]):
         ThisBitMap.set_at([Region[Config.REGION_X_OFFSET] - 1, Region[Config.REGION_Y_OFFSET] + y], Config.LINE_COLOUR)
         ThisBitMap.set_at([Region[Config.REGION_X_OFFSET] + Region[Config.REGION_X_LEN] + 1, Region[Config.REGION_Y_OFFSET] + y], Config.LINE_COLOUR)
      for x in range(Region[Config.REGION_X_LEN]):
         ThisBitMap.set_at([Region[Config.REGION_X_OFFSET] + x, Region[Config.REGION_Y_OFFSET] - 1], Config.LINE_COLOUR)
         ThisBitMap.set_at([Region[Config.REGION_X_OFFSET] + x, Region[Config.REGION_Y_OFFSET] + Region[Config.REGION_Y_LEN] + 1], Config.LINE_COLOUR)
   ThisSurface.blit(ThisBitMap, [0, 0])
   pygame.display.flip()


