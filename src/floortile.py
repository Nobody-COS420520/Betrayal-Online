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

    def add(self, a, dir_relation="up"):
        """ Adds parameter a into neighbors list """
        if a is None:
            return
        # print("In NeighborsComposite.add:  " + a.name + " " + dir_relation)
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
                # In case of floorchange or warp
                self.neighbors.append(a)
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
    # TODO Might not need to store this in instance
    doors = []                      # List with bools representing edges with a doorways
    # DoorList index format:
    # 0 - up
    # 1 - left
    # 2 - right
    # 3 - down
    img = ""                        # String containing URL to room image
    neighbors = None                # Reference to a NeighborsComposite instance
    gridspace = None

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

    # FloorTileLeaf.room_logic set in constructor ^
