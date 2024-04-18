# pylint: disable=C0301, E0602, W0603
"""  The first file concatted into the final .py that gets run  """
#    pygame zero only works with one module so all .py in /src are
#    concatenated into one single .py module upon docker run/start.

import pgzrun
import pygame
import math
import collections
import json
import os.path
import random
import sqlite3


WIDTH = 1920
HEIGHT = 1080
TITLE = "Betrayal Online"
PREV_GAME_STAGE = -1
GAME_STAGE = -1
#   -1 = used to detect when program is first opened (gets changed in first loop of update())
# 0 = program setup (pre main menu)
# 1 = main menu
# 2 = mid game
STAGEOBJ = None			# Holds object for current stage
DBURL = "src/db/betrayal.db"
