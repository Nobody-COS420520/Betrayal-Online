""" Module containing the FloorTile class hierarchy (Composite Structure) """


class FloorTileComponent():
    """ Base FloorTile Component class """

    def room_logic(self):
        """ Default placeholder room_logic method for FloorTiles, does nothing until overwritten """

    def execute(self, func, **kwargs):
        """ Executes passed function, func, from within a FloorTileComponent Object  """
        # To use this, format the func call like this: execute(lambda param: print(param),param="a")
        func(**kwargs)


class NeighborsComposite(FloorTileComponent):
    """ Composite class holding adjacent FloorTileComponents objects to a FloorTileLeaf object """

    neighbors = []               # Holds reference to adjacent FloorLeafComponent objects
    # Neighbors index format:
    # 0 = Up
    # 1 = Left
    # 2 = Right
    # 3 = Down
    # 4+ = Special adjacencies (across floors or warps)

    def __init__(self, p_neighbors=-1):
        """ NeighborsComposite Constructor """

        if (p_neighbors == -1):
            self.neighbors = [None]*4
        else:
            self.neighbors = p_neighbors

    def add(self, a, dir_relation="up", p_special_num=None):
        """ Adds parameter a into neighbors list """
        if a is None:
            return
        if (isinstance(a, FloorTileComponent)):
            if (dir_relation == "Up" or dir_relation == "up"):
                self.neighbors[0] = a
            elif (dir_relation == "Left" or dir_relation == "left"):
                self.neighbors[1] = a
            elif (dir_relation == "Right" or dir_relation == "right"):
                self.neighbors[2] = a
            elif (dir_relation == "Down" or dir_relation == "down"):
                self.neighbors[3] = a
            elif (dir_relation == "Special" or dir_relation == "special"):
                if p_special_num is None:
                    print(
                        "ERROR in NeighborsComposite.add():  p_special_num required but not passed")
                    return -1
                # In case of floorchange or warp
                for x in range(p_special_num-len(self.neighbors)):
                    self.neighbors.append(None)
                self.neighbors.append(a)
                # print("In NeighborsComposite:  " + str(p_special_num) + ", " + str(self.neighbors))
            else:
                print(
                    "Invalid dir_relation value (NeighborsComposite.add):  " + str(dir_relation))

    def remove(self, r=None, dir_relation=None):
        """ Removes parameter r from neighbors list """
        if isinstance(r, FloorTileComponent):
            self.neighbors.remove(r)
        elif (dir_relation == "Up" or dir_relation == "up"):
            self.neighbors[0] = None
        elif (dir_relation == "Left" or dir_relation == "left"):
            self.neighbors[1] = None
        elif (dir_relation == "Right" or dir_relation == "right"):
            self.neighbors[2] = None
        elif (dir_relation == "Down" or dir_relation == "down"):
            self.neighbors[3] = None
        elif (dir_relation == "Special" or dir_relation == "special"):
            print("ERROR: To remove Special neighbors, specify specific nodes to remove (NeighborsComposite.remove)")
        else:
            print("Invalid parameters (NeighborsComposite.remove)")

    def get_neighbors(self, recursion_cap=0):
        """ Returns a set of all FloorTileComponent objs recursively until recursion_cap is reached """
        working_set = set()
    ##################################################################

        def neighbors_recursive(p_composite, recursion_cap):
            """ Local recursive helper function for NeighborsComposite.get_neighbors() """
            nonlocal working_set
            if (recursion_cap < 1):
                return

            for x in p_composite.neighbors:
                working_set.add(x)
                if (x is not None):
                    neighbors_recursive(x.neighbors, recursion_cap-1)
            return
    ###################################################################
        for x in self.neighbors:
            working_set.add(x)
            if (x is not None):
                neighbors_recursive(x.neighbors, recursion_cap-1)

        return working_set

    def room_logic(self, recursion_cap=-1):
        """ Recursively calls all FloorTileComponent obj's room_logic method in neighbors """
        working_set = self.get_neighbors(recursion_cap)
        for x in working_set:
            x.room_logic()

    def execute(self, func, recursion_cap=-1, **kwargs):
        """ Recursively calls all FloorTileComponent obj's execute method in neighbors """
        # To use this, format the func call like this: execute(lambda param: print(param),param="a")
        working_set = self.get_neighbors(recursion_cap)
        for x in working_set:
            x.execute(func, **kwargs)

    def __iter__(self):
        self.iterator_index = -1
        return self

    def __next__(self):
        self.iterator_index += 1
        if (self.iterator_index == len(self.neighbors)):
            raise StopIteration
        return self.neighbors[self.iterator_index]


class FloorTileLeaf(FloorTileComponent):
    """ Leaf class holding most of the actual FloorTile data """

    id = -1                         # Unique id for the FloorTileLeaf object's room
    name = ""                       # String with the room's name
    # Represents the valid floors (FloorGrid) a FloorTIle can be played on
    floorlevel = 0
    # FloorLevels:
    #   0 - Basement ONLY
    #   1 - Basement + Ground Floor
    #   2 - Ground Floor ONLY
    #   3 - Ground Floor + Upper Floor
    #   4 - Upper Floor ONLY
    #   5 - Basement + Upper Floor
    #   6 - Basement + Ground + Upper
    doors = []                      # List with bools representing edges with a doorways
    # DoorList index format:
    # 0 - up
    # 1 - left
    # 2 - right
    # 3 - down
    img = ""                        # String containing URL to room image
    neighbors = None                # Reference to a NeighborsComposite instance
    gridspace = None                # Reference to the relevant GridSpace object
    # List of all Character objects located on the FloorTIleLeaf
    inhabitants = None
    angle = 0                       # Angle of rotation of

    def __init__(self, p_room_logic=-1, p_db_tuple=-1):
        """ FloorTileLeaf Constructor """
        self.neighbors = NeighborsComposite()
        if (callable(p_room_logic)):
            self.room_logic = p_room_logic
        if (p_db_tuple != -1):
            # print("Inside FloorTileLeaf Constructor:  " + str(p_db_tuple))
            self.id = p_db_tuple[0]
            self.name = p_db_tuple[1]
            self.floorlevel = p_db_tuple[2]
            self.doors = json.loads(p_db_tuple[3])
            self.img = p_db_tuple[4]
        self.gridspace = None
        self.inhabitants = []
        self.angle = 0

    # FloorTileLeaf.room_logic set in constructor ^

    def update_enclosed_actors(self):
        """ Displays enclosed actors in responsive manner (place in center / left half - right half, etc) """
        if len(self.inhabitants) == 0:
            return

        start_x = self.gridspace.get_x()
        start_y = self.gridspace.get_y()
        width = self.gridspace.actor.width

        # split floortile space into ceil(sqrt(n)) columns (num_hori)
        # and ceil(n/ceil(sqrt(n))) rows (num_vert)
        n = len(self.inhabitants)  # for readability
        num_hori = math.ceil(n**(0.5))
        num_vert = math.ceil(n/num_hori)
        l_width = self.gridspace.actor.width//num_hori
        # Might not need l_height due to squares but is here in case things change at some weird point
        l_height = self.gridspace.actor.height//num_vert

        h_count = 0
        v_count = 0
        for x in self.inhabitants:
            # Setup hori position
            working_x = self.gridspace.actor.x + h_count*l_width
            h_count += 1
            if h_count >= num_hori:
                h_count = 0

            # Setup vert position
            working_y = self.gridspace.actor.y + v_count*l_height
            v_count += 1
            if v_count >= num_vert:
                v_count = 0

            x.establish_actor((working_x, working_y), l_width)

        # Also zoom the logo if needed

    def rotate_doors(self, direction=None):
        """ Rotates a FloorTileLeaf instance either direction='Left' or direction='Right'"""

        if direction == "Right" or direction == "right":
            temp = self.doors[0]+0
            self.doors[0] = self.doors[2]
            self.doors[2] = self.doors[3]
            self.doors[3] = self.doors[1]
            self.doors[1] = temp

        elif direction == "Left" or direction == "left":

            temp = self.doors[3]+0
            self.doors[3] = self.doors[2]
            self.doors[2] = self.doors[0]
            self.doors[0] = self.doors[1]
            self.doors[1] = temp
