# File spec of h264 video files to process.
# Now an application argument.
# FILESPEC_H264 = "/media/user/BONET_DENT/2019-09-03_*.h264"

FILESPEC_BMP = "./DETECTED/*.png"
BMP_RESOLUTION = [640, 480]

# Debug, for rescanning the BMP files without pre-processing the h264 video.
SKIP_PROCESSING = False
# Allow the video to settle at the start of a video file by skipping a number
# of potentially unstable frames.
SKIP_FIRST_FRAMES = 15

# Define the area on the BMP files to scan for movement.
# Percentage difference between two frames to indicate movement (Sensitivity).
# [ X_OFFSET, Y_OFFSET, X_LEN, Y_LEN, STEP, MIN_PERCENT_DIFF ]
REGION_X_OFFSET = 0
REGION_Y_OFFSET = 1
REGION_X_LEN = 2
REGION_Y_LEN = 3
REGION_STEP = 4
REGION_MIN_PERCENT_DIFF = 5

REGIONS = [
   [
   ],
   [
      [ 235, 320, 120, 40, 3, 0.9 ],
      [ 190, 320, 40, 155, 3, 0.9 ],
      [ 410, 365, 40, 110, 3, 0.9 ],
   ],
   [
      [ 145, 320, 210, 40, 3, 2.0 ],
   ]
]

BLACK_COLOUR = (0x00, 0x00, 0x00)
BAR_COLOUR = (0x00, 0xFF, 0x00)
LINE_COLOUR = (0xFF, 0x00, 0x00)
TEXT_COLOUR = (0xFF, 0xFF, 0xFF)
TEXT_LINE_HEIGHT = 24
TEXT_LINE_COUNT = 3

