""" Holds functions related to drawing grid squares """
# pylint: disable=C0301, E0602, W0603

                    #   GRID globals get officially assigned in setup_midame()
                    #   these are default values
GRID_OFFSET_X = 0   #   Offset of grid that is not shown after zoom(left side)
GRID_OFFSET_Y = 0   #   Offset of grid that is not shown after zoom(top side)
GRID_SIZE = 128     #   Size of each grid square (px)
GRID_SCALE = 1      #   Scale of the grid (% decimal form)
GRID = []           #   2d Array of references to each square's GridSquare class
                    #   (initialized in initialize_grid())
bg = Actor("bo_specific/dark_wood_texture_1920x1080.jpg")

class GridSquare():
    """ Holds functions for a Grid Square's events and references to neighbor Grid Squares"""

    on_hover = None
    on_mouseup = None
    neighbors = None    #   Holds reference to neighbors in list with format [up, left, right, down]
    hori = 0            #   Number that represents this square's position IN GRID
    vert = 0
    highlight_color = "#c2f6b47f"
    actor = None     #   Holds Actor for floor tile, None if no floor tile
    rect = None         #   Holds pygame.Rect object for each square
    highlight_flag = 0

    # pylint: disable-next=W0102
    def __init__(self, p_hori = 0, p_vert = 0, p_neighbors = [None]*4,          \
            p_on_hover = -1,\
            p_on_offhover = -1,\
            p_on_mousedown = lambda p_x, p_y: print("Mousedown on square " + str(p_x) + ", " + str(p_y)), \
            p_on_mouseup = lambda p_x, p_y: print("Mouseup on square " + str(p_x) + ", " + str(p_y))):

        if p_on_hover == -1:
            self.on_hover = self.highlight
        if p_on_offhover == -1:
            self.on_offhover = self.unhighlight
        self.on_mousedown = p_on_mousedown
        self.on_mouseup = p_on_mouseup
        self.neighbors = p_neighbors
        self.hori = p_hori
        self.vert = p_vert
        self.rect = Rect(self.get_x(), self.get_y(), GRID_SIZE, GRID_SIZE)
        self.highlight_flag = 0

    def get_x(self):
        """ Returns x coordinate (pixels) for a GridSquare obj """
        return self.hori*GRID_SIZE+GRID_OFFSET_X

    def get_y(self):
        """ Returns y coordinate (pixels) for a GridSquare obj """
        return self.vert*GRID_SIZE+GRID_OFFSET_Y

    #def set_x(self, p_hori_px):
    #    """ Sets self.hori (the grid loc) using a px measurement """
    #    self.hori = p_hori_px+GRID_OFFSET_X/GRID_SIZE
    #    return self.hori

    #def set_y(self, p_vert_px):
    #    """ Sets self.vert (the grid loc) using a px measurement """
    #    self.vert = p_vert_px+GRID_OFFSET_Y/GRID_SIZE
    #    return self.vert
    
    def set_contents(self, p_image_url, **kwargs):
        """ Sets image Actor for Grid Square """
        pos = (self.get_x(), self.get_y())
        anchor = ""

        self.contents = Actor(p_image_url, pos, anchor, kwargs)
        return self.contents

    def update_actor(self):
        """ updates image actor for Grid Square """
        pos = (self.get_x(), self.get_y())
        anchor = "topleft"
        self.contents = Rect(pos, anchor)
        #os(pos)
        #self.contents.anchor(anchor)
        return self.contents

    def highlight(self):
        """ Flags GridSquare obj to be filled with self.highlightcolor """
        self.highlight_flag = 1


    def unhighlight(self):
        """ lowers flag for GridSquare obj to be filled with self.highlightcolor """
        self.highlight_flag = 0


    def __str__(self):
        return str((self.hori, self.vert))

    def __eq__(self, other):
        return self.hori == other.hori and self.vert == other.vert



def initialize_grid(p_width, p_height):
    """ Initializes and fills the global GRID 2d array with GridSquare objects """

    global GRID
    global GRID_SCALE
    global GRID_SIZE
    global GRID_OFFSET_X
    global GRID_OFFSET_Y

    GRID = []
    GRID_SCALE = 1
    GRID_SIZE = 128
    GRID_OFFSET_X = 0
    GRID_OFFSET_Y = 0

     #  Initializes GRID with empty GridSquare objects
    for x in range(0, math.ceil(p_width/GRID_SIZE)):
        GRID.append([])
        for y in range(0, math.ceil(p_height/GRID_SIZE)):
            GRID[x].append(GridSquare(x, y))

    print("State of GRID after initialization:  ", end="")
    for x in range(0, math.ceil(p_width/GRID_SIZE)):
        for y in range(0, math.ceil(p_height/GRID_SIZE)):
            print(str(GRID[x][y]) + ", ", end="")

    #print()
    return GRID

def establish_grid_neighbors(p_width, p_height):
    """ fills neighbors array for every GridSquare obj in GRID"""

    #TODO maybe change this to GRID instead of shown squares
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


def zoom(grid_size_modifier):
    """ Updates global GRID_SCALE var and scales+moves Rect objs in GRID
        grid_size_modifer = percent (decimal form) modifier global GRID vars are multiplied against """
    global GRID_SIZE
    global GRID_SCALE
    global GRID_OFFSET_X
    global GRID_OFFSET_Y

    GRID_SIZE *= grid_size_modifier
    GRID_SCALE *= grid_size_modifier
    GRID_OFFSET_X *= grid_size_modifier
    GRID_OFFSET_Y *= grid_size_modifier

    #   reset highlight flags for GRID squares to prevent lingering remnants
    #for x in range(len(GRID)):
    #    for y in range(len(GRID[0])):
    #        GRID[x][y].highlight_flag = 0
    
    # pylint: disable-next=C0200
    for x in range(len(GRID)):
    
        for y in range(len(GRID[x])):
            #   uncomment these if it turns out outer scope functions don't use
            #   up to date global vars (the changes here are small and make 
            #    little difference if it does or not)
            #x_pos = GRID[x][y].hori*GRID_SIZE+GRID_OFFSET_X
            #y_pos = GRID[x][y].vert*GRID_SIZE+GRID_OFFSET_Y
            x_pos = GRID[x][y].get_x()
            y_pos = GRID[x][y].get_y()
            GRID[x][y].rect = Rect(x_pos, y_pos, GRID_SIZE, GRID_SIZE)

    return GRID_SCALE

def cam_move_hori(p_delta_px):
    """ 
        Moves camera left/right (Grid moves right/left), p_delta_px is pixels to move
        p_delta_px > 0:  camera left
        p_delta_px < 0:  camera right
    """
    global GRID_OFFSET_X
    GRID_OFFSET_X +=p_delta_px
    
    for x in range(len(GRID)):
        for y in range(len(GRID[x])):
            GRID[x][y].rect.move_ip(p_delta_px, 0)
    
    return p_delta_px


def cam_move_vert(p_delta_px):
    """ 
        Moves camera up/down (Grid moves down/up), p_delta_px is pixels to move
        p_delta_px > 0:  camera up
        p_delta_px < 0:  camera down
    """
    global GRID_OFFSET_Y
    GRID_OFFSET_Y +=p_delta_px
    
    for x in range(len(GRID)):
        for y in range(len(GRID[x])):
            GRID[x][y].rect.move_ip(0, p_delta_px)
    
    return p_delta_px

def get_grid_loc(p_pos):
    """ 
        Gets grid loc coordinates (GRID[x][y] coordinates) for a given x,y coord pair
        p_pos = tuple (x coord, y coord)
    """

    return_x = int((p_pos[0]-GRID_OFFSET_X)//GRID_SIZE)
    #if return_x >= len(GRID):
    #    return_x = len(GRID)-1

    return_y = int((p_pos[1]-GRID_OFFSET_Y)//GRID_SIZE)
    #if return_y >= len(GRID[0]):
    #    return_y = len(GRID[0])-1

    return (return_x, return_y)


#def place_floor_tile(p_x, p_y, p_tile = None):
#    """ Places floor tile at coordinate (p_x,p_y) """
#    pass
