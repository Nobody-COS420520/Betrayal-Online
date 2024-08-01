""" Holds functions related to drawing grid squares """
# pylint: disable=C0301, E0602, W0603


class Midgame():
    """ (not) Singleton class holding properties of the midgame Game Stage (stage number 2) """

    #   Grid attributes get officially assigned in setup_midame()
    #   these are default values

    grid_offset_x = 0  # Offset of grid that is not shown after zoom(left side)
    grid_offset_y = 0  # Offset of grid that is not shown after zoom(top side)
    grid_size = 0  # Size of each grid square (px)
    grid_scale = 0  # Scale of the grid (% decimal form)
    grid = []  # 2d Array of references to each square's GridSquare class
    #   (initialized in initialize_grid())
    floorgrids = []     # Holds each of the FloorGrid objs in play
    floor_index = 0     # Holds index for currently displayed floor
    # Format:
    # 0 = Basement
    # 1 = Ground
    # 2 = Upper
    # Holds Collections.deque instance with Character objs and the turn order
    turn_q = None
    turn = []               # Holds list of GameTurn objs that have occured
    foreground_ui = None    # Holds dict of UI elements' Actors to draw above of the Grid
    option_tree = None      # Holds MenuTree obj for foreground elements
    game_stage = 0          # Holds integer flag representing current stage of the game
    # game_stage Format:
    # 0 = exploration phase
    # 1 = pre-haunt phase
    # 2 = haunt phase

    midgame_bg = Actor("bo_specific/dark_wood_texture_1920x1080.jpg")

    def __init__(self, turn_queue=-1):
        """ Midgame class Constructor, turn_queue gets created during CharacterSelect phase """
        self.initialize_grid(WIDTH, HEIGHT)
        self.establish_grid_neighbors(WIDTH, HEIGHT)
        self.setup_floorgrid()
        self.assign_floorgrid_to_grid(self.floorgrids[self.floor_index])
        if (turn_queue == -1):
            self.turn_q = collections.deque()
            db = DBManager(DBURL)
            data = db.retrieve_character_data()
            db.close()
            for x in data:
                self.turn_q.append(Character(x))
        # Creation of midgame MenuTree
        self.option_tree = Menu_Tree()
        self.option_tree.add("Menu", Rect(                  # option_tree[0]
            (WIDTH//71.1, HEIGHT//37.24), (WIDTH//13.24, HEIGHT//16.6)))
        self.option_tree.add("Next", Rect(                  # option_tree[1]
            (WIDTH//1.16, 0), (WIDTH//7.11, HEIGHT//7.4)))
        self.option_tree.add("moves remaining", Rect(       # option_tree[2]
            (WIDTH-(WIDTH//4.9), HEIGHT//10), (WIDTH//4.9, HEIGHT//6.3)))
        self.option_tree.contents[0].adjacencies[1] = self.option_tree.contents[1]
        self.option_tree.contents[0].adjacencies[2] = self.option_tree.contents[1]
        self.option_tree.contents[1].adjacencies[1] = self.option_tree.contents[0]
        self.option_tree.contents[1].adjacencies[2] = self.option_tree.contents[0]
        for x in self.option_tree.contents:
            x.text.midgame_default(x)
            x.text.fontsize = x.text.fontsize*(HEIGHT/1080)
            x.text.top = self.option_tree.contents[0].rect.top
        self.option_tree.contents[0].text.centerx = self.option_tree.contents[0].rect.centerx
        self.option_tree.contents[1].text.right = WIDTH-(WIDTH//12) # 11.77
        self.option_tree.contents[1].on_mouseup = lambda x: self.end_turn()
        self.option_tree.contents[2].on_hover = lambda x: 1
        self.option_tree.contents[2].on_offhover = lambda x: 1
        self.option_tree.contents[2].text.midright = self.option_tree.contents[2].rect.midright

        # self.option_tree.contents[2].text.bottomright = self.option_tree.contents[2].rect.bottomright

        # Creation of Characters
        self.initial_character_placement()
        self.foreground_ui = dict()

        # Beginning of first turn
        self.turn = [GameTurn(self.turn_q[0], self.game_stage, self)]

        # Setup Demo
        self.setup_demo()

    ##### \/\/ DEMO STUFF \/\/ #####
    def setup_demo(self):
        """ Demo stuff to be done in the MidGame initialization """
        for x in self.turn_q:
            x.win_check.append(lambda: exec("""
def test():
    for x in STAGEOBJ.turn_q:
        if x.affiliation == 'Explorer' and x.current_loc.name != 'Doorway':
            return False
    return True

if test() == True:                                          
    STAGEOBJ.game_over('Explorer')                                        
"""))

    def game_over(self, winning_affiliation):
        """ Code to execute on successful win check, when one affiliation wins """
        global GAME_STAGE

        print(str(winning_affiliation) + "s win")
        GAME_STAGE = 1
        tkinter.messagebox.showinfo("Game Finish", str(winning_affiliation) + "s Win!")
    ##### /\/\ DEMO STUFF /\/\ #####

    class GridSquare():
        """ Holds functions for a Grid Square's events and references to neighbor Grid Squares"""

        on_hover = None
        on_mouseup = None
        # Holds reference to neighbors in list with format [up, left, right, down]
        neighbors = None
        hori = 0  # Number that represents this square's position IN GRID
        vert = 0
        highlight_color = "#c2f6b47f"
        floortile = None  # Holds FloorTile obj assigned to grid space, None if no floor tile
        rect = None  # Holds pygame.Rect object for each square
        highlight_flag = 0
        grid = None
        actor = None    # Holds actor for contents of GridSquare

        # pylint: disable-next=W0102
        def __init__(self, p_hori=0, p_vert=0, p_grid=None,
                     p_neighbors=[None]*4,
                     p_on_hover=-1,
                     p_on_offhover=-1,
                     p_on_mousedown=None,
                     p_on_mouseup=None):

            if p_on_hover == -1:
                self.on_hover = self.highlight
            if p_on_offhover == -1:
                self.on_offhover = self.unhighlight
            if p_on_mousedown is None:
                self.on_mousedown = lambda p_x, p_y: print(
                    "Mousedown on square " + str(p_x) + ", " + str(p_y) + ", " +
                    self.floortile.name if self.floortile is not None else "None")
            else:
                self.on_mousedown = p_on_mousedown
            if p_on_mouseup is None:
                self.on_mouseup = lambda p_x, p_y: print(
                    "Mouseup on square " + str(p_x) + ", " + str(p_y) + ", " +
                    self.floortile.name if self.floortile is not None else "None")
            else:
                self.on_mouseup = p_on_mouseup
            self.neighbors = p_neighbors
            self.hori = p_hori
            self.vert = p_vert
            self.grid = p_grid
            self.rect = Rect(self.get_x(), self.get_y(),
                             self.grid.grid_size, self.grid.grid_size)
            self.highlight_flag = 0
            self.actor = None

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
    ##############################################################################

    @staticmethod
    def on_hover(p_menu_object):
        """ Executes on hover over MidGame menu object """
        p_menu_object.text.fontsize = 64*(HEIGHT/1080)

    @staticmethod
    def on_offhover(p_menu_object):
        """ Executes on offhover over MidGame menu object """
        p_menu_object.text.fontsize = 52*(HEIGHT/1080)
        p_menu_object.highlight_flag = 0

    @staticmethod
    def on_mouseup(p_menu_object):
        """ Executes on hover over MidGame menu object """
        p_menu_object.highlight_flag = 1

    @staticmethod
    def next_mouseup(p_menu_object):
        """ Triggers end of turn logic """

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

        return self.grid

    def establish_grid_neighbors(self, p_width, p_height):
        """ fills neighbors array for every GridSquare obj in GRID 
            index format:
            0 = Up
            1 = Left
            2 = Right
            3 = Down
        """
        for x in range(0, p_width//self.grid_size):
            for y in range(0, p_height//self.grid_size):
                neighbors = [None]*4
                neighbors[0] = self.grid[x][y -
                                            1] if y != 0 else None    # Up neighbor
                neighbors[1] = self.grid[x -
                                         # Left neighbor
                                         1][y] if x != 0 else None
                # Right Neighbor
                neighbors[2] = self.grid[x +
                                         1][y] if x != p_width//self.grid_size-1 else None
                # Bottom Neighbor
                neighbors[3] = self.grid[x][y +
                                            1] if y != p_height//self.grid_size-1 else None

                self.grid[x][y].neighbors = neighbors

    def setup_floorgrid(self):
        """ Sets up the 3 FloorGrid objects and self.floorgrids """
        self.floorgrids = []
        self.floorgrids.append(FloorGrid("Basement", 0))
        self.floorgrids.append(FloorGrid("Ground", 1))
        self.floorgrids.append(FloorGrid("Upper", 2))
        for x in self.floorgrids:
            x.setup_floor_neighbors(self.floorgrids)
        self.floor_index = 1

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
                # x_pos = GRID[x][y].hori*GRID_SIZE+GRID_OFFSET_X
                # y_pos = GRID[x][y].vert*GRID_SIZE+GRID_OFFSET_Y
                x_pos = self.grid[x][y].get_x()
                y_pos = self.grid[x][y].get_y()
                self.grid[x][y].rect = Rect(
                    x_pos, y_pos, self.grid_size, self.grid_size)
                if (self.grid[x][y].actor is not None):
                    self.establish_actor(self.grid[x][y])
                    self.grid[x][y].floortile.update_enclosed_actors()

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
                if (self.grid[x][y].actor is not None):
                    self.establish_actor(self.grid[x][y])
                    self.grid[x][y].floortile.update_enclosed_actors()

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
                if (self.grid[x][y].actor is not None):
                    self.establish_actor(self.grid[x][y])
                    self.grid[x][y].floortile.update_enclosed_actors()

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

    def assign_floorgrid_to_grid(self, p_floorgrid, focus=None):
        """ Switchs the floortiles displayed in grid to the floortiles in p_floorgrid
            focus should be FloorTile obj that will be placed in the center of screen """

        # Establish visited_matrix which will contain flags to keep track of traveled tiles
        # Also wiping grid of current floortiles and actors during same iteration of grid
        visited_matrix = [[]]*len(self.grid)
        for x in range(len(visited_matrix)):
            visited_matrix[x] = [False]*len(self.grid[x])
            for y in range(len(self.grid[x])):
                self.grid[x][y].floortile = None
                self.grid[x][y].actor = None

     # local helper function
        def recursive_traversal(p_floortile, p_gridspace):

            nonlocal visited_matrix

            if (p_floortile is None or p_gridspace is None or visited_matrix[p_gridspace.hori][p_gridspace.vert] is True):
                return

            p_gridspace.floortile = p_floortile
            p_floortile.gridspace = p_gridspace
            self.establish_actor(p_gridspace, p_floortile)
            p_floortile.update_enclosed_actors()

            visited_matrix[p_gridspace.hori][p_gridspace.vert] = True

            for x in p_floortile.neighbors:
                if (p_gridspace.vert-1 >= 0):
                    recursive_traversal(
                        p_floortile.neighbors.neighbors[0], p_gridspace.neighbors[0])
                if (p_gridspace.hori-1 >= 0):
                    recursive_traversal(
                        p_floortile.neighbors.neighbors[1], p_gridspace.neighbors[1])
                if (p_gridspace.hori+1 < len(self.grid)):
                    recursive_traversal(
                        p_floortile.neighbors.neighbors[2], p_gridspace.neighbors[2])
                if (p_gridspace.vert+1 < len(self.grid[p_gridspace.hori])):
                    recursive_traversal(
                        p_floortile.neighbors.neighbors[3], p_gridspace.neighbors[3])
         # local helper function

        # Assigns focus to default focus if a focus was not passed with call
        if focus is None:
            if p_floorgrid.floorid == "Ground":
                focus = p_floorgrid.contents[1]
            else:
                focus = p_floorgrid.contents[0]

        grid_coords = self.get_grid_loc((WIDTH//2, HEIGHT//2))
        recursive_traversal(focus, self.grid[grid_coords[0]][grid_coords[1]])

    def establish_actor(self, p_gridspace, p_floortile=None):
        """ Assigns FloorTile actor data to p_gridspace with correct position and scale """
        if (p_floortile is None):
            p_floortile = p_gridspace.floortile

        p_gridspace.actor = Actor(
            p_floortile.img, topleft=p_gridspace.rect.topleft, anchor=(0, 0))

        p_gridspace.actor._surf = pygame.transform.scale(
            p_gridspace.actor._surf, (self.grid_size, self.grid_size))
        p_gridspace.actor._surf = pygame.transform.rotate(
            p_gridspace.actor._surf, p_floortile.angle)
        p_gridspace.actor._update_pos()
        p_gridspace.actor.x = p_gridspace.get_x()
        p_gridspace.actor.y = p_gridspace.get_y()

    def draw_floortile(self, p_gridspace):
        """ Draws a random FloorTile id and creates a FloorTIle obj from data in DB """

        # Determine random possible FloorTile id
        current_floor = self.floorgrids[self.floor_index]
        random_id = current_floor.possible[random.randrange(
            len(current_floor.possible))]

        # Remove possible id from other FloorGrid's list of possible ids
        current_floor.remove_poss_floortile(random_id)

        # Build FloorTileLeaf obj from data retrieved from the random id
        db = DBManager(DBURL)
        working_floortile = FloorTileLeaf(
            p_db_tuple=db.retrieve_floortile_data_id(random_id))
        db.close()

        # Finish Assimilating working_floortile into FloorGrid, setting up neighbors + refs and display
        working_floortile.gridspace = p_gridspace
        p_gridspace.floortile = working_floortile
        self.establish_actor(p_gridspace)
        if (p_gridspace.neighbors[0] is not None):
            working_floortile.neighbors.add(
                p_gridspace.neighbors[0].floortile, dir_relation="Up")
        if (p_gridspace.neighbors[1] is not None):
            working_floortile.neighbors.add(
                p_gridspace.neighbors[1].floortile, dir_relation="Left")
        if (p_gridspace.neighbors[2] is not None):
            working_floortile.neighbors.add(
                p_gridspace.neighbors[2].floortile, dir_relation="Right")
        if (p_gridspace.neighbors[3] is not None):
            working_floortile.neighbors.add(
                p_gridspace.neighbors[3].floortile, dir_relation="Down")

        return working_floortile

    def display_floorgrid(self, p_grid_index, p_focus=None):
        """ Switches the displayed floorgrid, switching all floortiles displayed """
        self.assign_floorgrid_to_grid(self.floorgrids[p_grid_index], p_focus)

    def initial_character_placement(self):
        """ At the start of MidGame phase, place all characters inside turn_q in the Entrance Hall """
        # Sets all character's current_loc to the Entrance Hall
        for x in self.turn_q:
            self.place_character(x, self.floorgrids[1].contents[1])
            x.current_floor = 1

    def place_character(self, p_character, p_floortile):
        """ Places p_character in p_floortile, updating both new and previous FloorTile """
        # Remove p_character from their current FloorTile
        prev_floortile = p_character.current_loc
        if prev_floortile is not None:
            prev_floortile.inhabitants.remove(p_character)
            prev_floortile.update_enclosed_actors()

        # Place p_character into p_floortile
        p_character.current_loc = p_floortile
        p_floortile.inhabitants.append(p_character)
        p_floortile.update_enclosed_actors()

    def rotate(self, p_direction, p_gridspace=None, p_floortile=None, num_rotates=1):
        """ Rotates floortile inside p_gridspace either p_direction='Left' or 'Right '"""

        if p_gridspace and p_floortile is None:
            p_floortile = p_gridspace.floortile
        elif p_floortile and p_gridspace is None:
            p_gridspace = p_floortile.gridspace

        for x in range(num_rotates):
            # rotating doors should be done beforehand/after to determine how many rotates
            # uncommenting this will break rotating during GameTurn.move()
            # p_floortile.rotate_doors(p_direction)

            if p_direction == "Left" or p_direction == "left":
                p_floortile.angle -= 90
                if p_floortile.angle < 0:
                    p_floortile.angle += 360

            elif p_direction == "Right" or p_direction == "right":
                p_floortile.angle += 90
                if p_floortile.angle > 360:
                    p_floortile.angle -= 360

        STAGEOBJ.establish_actor(p_gridspace)

    def end_turn(self):
        """ Executes end of turn behavior and sets up a new turn """
        turn = self.turn[len(self.turn)-1]
        turn.wrap_up_turn()
        self.turn_q.rotate(-1)
        self.turn.append(GameTurn(self.turn_q[0], self))

    def opp_direction(self, p_direction=0):
        """ Returns the opposite direction value, used for going to a neighbor and back """
        match(p_direction):
            case 0:  # opp of up is down
                return 3
            case 1:  # opp of left is right
                return 2
            case 2:  # opp of right is left
                return 1
            case 3:  # opp of down is up
                return 0
            case 4:  # opp of down floor is up floor
                return 5
            case 5:  # opp of up floor is down floor
                return 4
