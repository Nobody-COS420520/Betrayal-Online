from distutils.core import setup
from setuptools import find_packages
import os
# Optional project description in README.md:
current_directory = os.path.dirname(os.path.abspath(__file__))
try:
    with open(os.path.join(current_directory, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except Exception:
    long_description = """

 Demo Version 0.1
 
 Select "DEMO" from Main Menu to begin:
 
 - Use Arrow Keys to move around game board
 
 - Use Left Shift + Up Arrow to move up a floor from the Grand Staircase or the Basement Landing

 - Use Left Shift + Down Arrow to move down a floor from the Grand Staircase or the Upper Landing

 - When you move to an unexplored space, Left and Right Arrows to rotate the tile, Enter Key to confirm
 
 - Press "Next" in the Upper Right corner of the screen to finish your turn
 
 - Game ends when all players have walked out the doorway (standing to the right of the Entrance Hall)
 
 - Numpad 8,4,6,2 to move the camera
 
 - Numpad 7 to zoom out
 
 - Numpad 9 to zoom in

"""

setup(
name='Betrayal-Online',
# Packages to include in the distribution: 
packages=find_packages(','),

version='0.1.0',

description='Demo version of Betrayal-Online, a University project.',

long_description=long_description,
long_description_content_type='text/markdown',

author='Nobody (Caleb Corlett, Ryan Nodarse, Patrick Storer, Ethan Wyman)',
classifiers=[
    "Programming Language :: Python :: 3"
]

install_requires=[
"<pgzero> >= <1.2.1>",
"<tk> >= <0.1.0>"
])