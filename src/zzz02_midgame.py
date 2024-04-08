""" Holds functions related to drawing grid squares """
# pylint: disable=C0301, E0602, W0603


class Midgame():
    """ Singleton class holding properties of the midgame Game Stage (stage number 2) """

    #   Grid attributes get officially assigned in setup_midame()
    #   these are default values

    grid_offset_x = 0  # Offset of grid that is not shown after zoom(left side)
    grid_offset_y = 0  # Offset of grid that is not shown after zoom(top side)
    grid_size = 0  # Size of each grid square (px)
    grid_scale = 0  # Scale of the grid (% decimal form)
    grid = []  # 2d Array of references to each square's GridSquare class
    #   (initialized in initialize_grid())

    midgame_bg = Actor("bo_specific/dark_wood_texture_1920x1080.jpg")

    def __init__(self):
        """ Midgame class Constructor """
        self.setup_midgame()

    class GridSquare():
        """ Holds functions for a Grid Square's events and references to neighbor Grid Squares"""

        on_hover = None
        on_mouseup = None
        # Holds reference to neighbors in list with format [up, left, right, down]
        neighbors = None
        hori = 0  # Number that represents this square's position IN GRID
        vert = 0
        highlight_color = "#c2f6b47f"
        actor = None  # Holds Actor for floor tile, None if no floor tile
        rect = None  # Holds pygame.Rect object for each square
        highlight_flag = 0
        grid = None

        # pylint: disable-next=W0102
        def __init__(self, p_hori=0, p_vert=0, p_grid=None,
                     p_neighbors=[None]*4,
                     p_on_hover=-1,
                     p_on_offhover=-1,
                     p_on_mousedown=lambda p_x, p_y: print(
                         "Mousedown on square " + str(p_x) + ", " + str(p_y)),
                     p_on_mouseup=lambda p_x, p_y: print("Mouseup on square " + str(p_x) + ", " + str(p_y))):

            if p_on_hover == -1:
                self.on_hover = self.highlight
            if p_on_offhover == -1:
                self.on_offhover = self.unhighlight
            self.on_mousedown = p_on_mousedown
            self.on_mouseup = p_on_mouseup
            self.neighbors = p_neighbors
            self.hori = p_hori
            self.vert = p_vert
            self.grid = p_grid
            self.rect = Rect(self.get_x(), self.get_y(),
                             self.grid.grid_size, self.grid.grid_size)
            self.highlight_flag = 0

        def get_x(self):
            """ Returns x coordinate (pixels) for a GridSquare obj """
            return self.hori*self.grid.grid_size+self.grid.grid_offset_x

        def get_y(self):
            """ Returns y coordinate (pixels) for a GridSquare obj """
            return self.vert*self.grid.grid_size+self.grid.grid_offset_y

        # def set_x(self, p_hori_px):
        #    """ Sets self.hori (the grid loc) using a px measurement """
        #    self.hori = p_hori_px+GRID_OFFSET_X/GRID_SIZE
        #    return self.hori

        # def set_y(self, p_vert_px):
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
            # os(pos)
            # self.contents.anchor(anchor)
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

    def setup_midgame(self):
        """ Sets all midgame variables to default values. 
            Used in seting up and resetting midgame stage. """

        print("beg of setup")
        self.initialize_grid(WIDTH, HEIGHT)
        print("mid of setup")
        self.establish_grid_neighbors(WIDTH, HEIGHT)
        print("end of setup")

    def initialize_grid(self, p_width, p_height):
        """ Initializes and fills the global GRID 2d array with GridSquare objects """

        self.grid = []
        self.grid_scale = 1
        self.grid_size = 128
        self.grid_offset_x = 0
        self.grid_offset_y = 0

        #  Initializes GRID with empty GridSquare objects
        for x in range(0, math.ceil(p_width/self.grid_size)):
            self.grid.append([])
            for y in range(0, math.ceil(p_height/self.grid_size)):
                self.grid[x].append(self.GridSquare(x, y, self))

        print("State of GRID after initialization:  ", end="")
        for x in range(0, math.ceil(p_width/self.grid_size)):
            for y in range(0, math.ceil(p_height/self.grid_size)):
                print(str(self.grid[x][y]) + ", ", end="")

        # print()
        return self.grid

    def establish_grid_neighbors(self, p_width, p_height):
        """ fills neighbors array for every GridSquare obj in GRID"""

        # TODO maybe change this to GRID instead of shown squares
        for x in range(0, p_width//self.grid_size):
            for y in range(0, p_height//self.grid_size):
                neighbors = [None]*4
                neighbors[0] = self.grid[x -
                                         1][y] if x != 0 else None   # up neighbor
                neighbors[1] = self.grid[x][y -
                                            1] if y != 0 else None    # left neighbor
                # Right Neighbor
                neighbors[2] = self.grid[x][y +
                                            1] if y != p_height//self.grid_size-1 else None
                # Bottom Neighbor
                neighbors[3] = self.grid[x +
                                         1][y] if x != p_width//self.grid_size-1 else None
                self.grid[x][y].neighbors = neighbors

    def zoom(self, grid_size_modifier):
        """ Updates global GRID_SCALE var and scales+moves Rect objs in GRID
            grid_size_modifer = percent (decimal form) modifier global GRID vars are multiplied against """

        self.grid_size *= grid_size_modifier
        self.grid_scale *= grid_size_modifier
        self.grid_offset_x *= grid_size_modifier
        self.grid_offset_y *= grid_size_modifier

        #   reset highlight flags for GRID squares to prevent lingering remnants
        # for x in range(len(GRID)):
        #    for y in range(len(GRID[0])):
        #        GRID[x][y].highlight_flag = 0

        # pylint: disable-next=C0200
        for x in range(len(self.grid)):

            for y in range(len(self.grid[x])):
                #   uncomment these if it turns out outer scope functions don't use
                #   up to date global vars (the changes here are small and make
                #    little difference if it does or not)
                # x_pos = GRID[x][y].hori*GRID_SIZE+GRID_OFFSET_X
                # y_pos = GRID[x][y].vert*GRID_SIZE+GRID_OFFSET_Y
                x_pos = self.grid[x][y].get_x()
                y_pos = self.grid[x][y].get_y()
                self.grid[x][y].rect = Rect(
                    x_pos, y_pos, self.grid_size, self.grid_size)

        return self.grid_scale

    def cam_move_hori(self, p_delta_px):
        """ 
            Moves camera left/right (Grid moves right/left), p_delta_px is pixels to move
            p_delta_px > 0:  camera left
            p_delta_px < 0:  camera right
        """
        self.grid_offset_x += p_delta_px

        for x in range(len(self.grid)):
            for y in range(len(self.grid[x])):
                self.grid[x][y].rect.move_ip(p_delta_px, 0)

        return p_delta_px

    def cam_move_vert(self, p_delta_px):
        """ 
            Moves camera up/down (Grid moves down/up), p_delta_px is pixels to move
            p_delta_px > 0:  camera up
            p_delta_px < 0:  camera down
        """
        self.grid_offset_y += p_delta_px

        for x in range(len(self.grid)):
            for y in range(len(self.grid[x])):
                self.grid[x][y].rect.move_ip(0, p_delta_px)

        return p_delta_px

    def get_grid_loc(self, p_pos):
        """ 
            Gets grid loc coordinates (GRID[x][y] coordinates) for a given x,y coord pair
            p_pos = tuple (x coord, y coord)
        """

        return_x = int((p_pos[0]-self.grid_offset_x)//self.grid_size)
        # if return_x >= len(GRID):
        #    return_x = len(GRID)-1

        return_y = int((p_pos[1]-self.grid_offset_y)//self.grid_size)
        # if return_y >= len(GRID[0]):
        #    return_y = len(GRID[0])-1

        return (return_x, return_y)

    # def place_floor_tile(p_x, p_y, p_tile = None):
    #    """ Places floor tile at coordinate (p_x,p_y) """
    #    pass
