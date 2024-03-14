# pylint: skip-file
"""  The first file concatted into the final .py that gets run  """
#    pygame zero only works with one module so all .py in /src are
#    concatenated into one single .py module upon docker run/start.

import pgzrun
from pygame import Rect, key
import math


WIDTH = 960
HEIGHT = 540
TITLE = "Betrayal Online"
PREV_GAME_STAGE = -1
GAME_STAGE = -1
    #   -1 = used to detect when program is first opened (gets changed in first loop of update())
	#	0 = program setup (pre main menu)
	#	1 = main menu
	#	2 = mid game
