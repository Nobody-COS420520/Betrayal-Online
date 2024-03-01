"""Module for functions related to Pygame 0 operations"""

import os
import pgzhelper
#import pygame as pg

main_dir = os.path.split(os.path.abspath(__file__))[0]

"""
def load_image(file):
    """loads an image, prepares it for play"""
    file = os.path.join(main_dir, "data", file)
    try:
        surface = pg.image.load(file)
    except pg.error:
        raise SystemExit(f'Could not load image "{file}" {pg.get_error()}')
    return surface.convert()
    """