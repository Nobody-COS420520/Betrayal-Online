""" Holds functions related to drawing grid squares """
#import sys
#sys.path.append('..')

# import math
#import pgzhelper
#import pygame

GRID_SIZE = 128     #   Size of each grid square (px)
GRID = []           #   2d Array of references to each square's GridSquare class 
                    #   (initialized in initialize_grid())

class GridSquare():
    """ Holds functions for a Grid Square's events and references to neighbor Grid Squares"""

    on_hover = None
    on_mouseup = None
    neighbors = None    #   Holds reference to neighbors in list with format [up, left, right, down]
    hori = 0            #   Number that represents this square's position IN GRID
    vert = 0
    highlight_color = "#c2f6b47f"

    # pylint: disable-next=W0102
    def __init__(self, p_hori = 0, p_vert = 0, p_neighbors = [None]*4,          \
                p_on_hover = lambda p_x, p_y: print("Hover on square " + str(p_x) + ", " + str(p_y)),\
                p_on_mouseup = lambda p_x, p_y: print("Mouseup on square " + str(p_x) + ", " + str(p_y))):
        self.on_hover = p_on_hover
        self.on_mouse_up = p_on_mouseup
        self.neighbors = p_neighbors
        self.hori = p_hori
        self.vert = p_vert

    def get_x(self):
        """ Returns x coordinate (pixels) for a GridSquare obj """
        return self.hori*GRID_SIZE
    
    def get_y(self):
        """ Returns y coordinate (pixels) for a GridSquare obj """
        return self.vert*GRID_SIZE

    def highlight_square(self):
        """ idk what I wanted to do with this yet """
        pass

    

    def __str__(self):
        return str((self.hori, self.vert))

    def __eq__(self, other):
        return self.hori == other.hori and self.vert == other.vert

#def draw():
#    """ Will replace pygame zero's draw function with midgame specific stuff """
#    print("abc")
#    #bg = Actor("bo_specific/dark_wood_texture.jpg", topleft=(0,0))
#    screen.blit("bo_specific/dark_wood_texture.jpg", (0,0))
#    while(True):
#        pass
#    #screen.clear()
    


def initialize_grid(p_width, p_height):
    """ Initializes and fills the global GRID 2d array with GridSquare objects """

     #  Initializes GRID with empty GridSquare objects
    for x in range(0, p_width//GRID_SIZE):
        GRID.append([])
        for y in range(0, p_height//GRID_SIZE):
            GRID[x].append(GridSquare(x, y))

     #  TODO delete this print for loop
    print("State of GRID after initialization:  ", end="")
    for x in range(0, p_width//GRID_SIZE):
        for y in range(0, p_height//GRID_SIZE):

            print(str(GRID[x][y]) + ", ", end="")

    print()
    return GRID

def establish_grid_neighbors(p_width, p_height):
    """ fills neighbors array for every GridSquare obj in GRID"""

    for x in range(0, p_width//GRID_SIZE):
        for y in range(0, p_height//GRID_SIZE):
            neighbors = [None]*4
            neighbors[0] = GRID[x-1][y] if x!=0 else None   # up neighbor
            neighbors[1] = GRID[x][y-1] if y!=0 else None    # left neighbor
            neighbors[2] = GRID[x][y+1] if y!= p_height//GRID_SIZE-1 else None   # Right Neighbor
            neighbors[3] = GRID[x+1][y] if x!= p_width//GRID_SIZE-1 else None   # Bottom Neighbor
            GRID[x][y].neighbors = neighbors


def setup_midgame(p_width, p_height):
    """ Holds all methods required to setup the midgame state """        

    print("beg of setup")
    initialize_grid(p_width, p_height)
    print("mid of setup")
    establish_grid_neighbors(p_width, p_height)
    print("end of setup")



#def draw_highlight_square(p_x = hori*GRID_SIZE, p_y =vert*GRID_SIZE):
#        
#    """
#        Highlight grid square based on mouse position
#        pX = mouse x coord
#        pY = mouse y coord
#
#    """

def place_floor_tile(p_x, p_y, p_tile = None):
    """ Places floor tile at coordinate (p_x,p_y) """
