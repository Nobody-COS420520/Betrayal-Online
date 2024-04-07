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

    def __init__(self, p_neighbors=-1):
        """ NeighborsComposite Constructor """

        if (p_neighbors == -1):
            self.neighbors = []
        else:
            self.neighbors = p_neighbors

    def add(self, a):
        """ Adds parameter a into neighbors list """
        if (isinstance(a, FloorTileComponent)):
            self.neighbors.append(a)

    def remove(self, r):
        """ Removes parameter r from neighbors list """
        if isinstance(r, FloorTileComponent):
            self.neighbors.remove(r)

    def get_neighbors(self, recursion_cap=0):
        """ Returns a set of all FloorTileComponent objs recursively until recursion_cap is reached """
        working_set = set()
    ##################################################################

        def neighbors_recursive(p_composite, recursion_cap):
            """ Local recursive helper function for NeighborsComposite.get_neighbors() """
            nonlocal working_set
            if (recursion_cap == 0):
                return

            for x in p_composite.neighbors:
                working_set.add(x)
                neighbors_recursive(x.neighbors, recursion_cap-1)
            return
    ###################################################################
        for x in self.neighbors:
            working_set.add(x)
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


class FloorTileLeaf(FloorTileComponent):
    """ Leaf class holding most of the actual FloorTile data """

    count_floortileleaf = 0         # Static count of all FloorTileLeaf objects
    id = ""                         # Unique String id for a FloorTileLeaf instance
    neighbors = None                # Reference to a NeighborsComposite instance

    def __init__(self, p_room_logic=-1):
        """ FloorTileLeaf Constructor """
        self.id = str(FloorTileLeaf.count_floortileleaf)
        FloorTileLeaf.count_floortileleaf += 1
        self.neighbors = NeighborsComposite()
        if (callable(p_room_logic)):
            self.room_logic = p_room_logic

    # FloorTileLeaf.room_logic set in constructor ^
