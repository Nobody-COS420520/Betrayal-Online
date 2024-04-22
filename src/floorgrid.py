""" Module containing the FloorGrid class and related methods """


class FloorGrid():
    """ Class for the FloorGrid containing a floor's FloorTile objects """

    # Holds String identifier for the floor ("Basement" | "Ground" | "Upper")
    floorid = ""
    index = 0               # Holds index of current floor in the MidGame obj
    neighbors = []          # Holds list of neighbor FloorGrid objs,
    # Index Format: 0 = lower neighbor, 1 = higher neighbor
    contents = []           # Contains FloorTiles inside FloorGrid
    possible = []           # Contains valid FloorTile ids remaining to be placed

    def __init__(self, p_floor, p_index):
        """ Constructor for FloorGrid """
        self.index = p_index
        self.contents = []
        data_tuple = []
        db = DBManager(DBURL)

        # Retrieving all valid FloorTile ids for p_floor
        if (p_floor == "Basement" or p_floor == "basement"):
            # Retrieve valid FloorTile ids for the floor and the starting Tile's data
            ids = db.retrieve_floortile_id_floorlevel(0, plus_adjacent=True)

            data_tuple.append(db.retrieve_floortile_data_id(0))
            for x in data_tuple:
                self.contents.append(FloorTileLeaf(p_db_tuple=x))

            self.floorid = "Basement"
        elif (p_floor == "Ground" or p_floor == "ground"):
            ids = db.retrieve_floortile_id_floorlevel(2, plus_adjacent=True)

            data_tuple.append(db.retrieve_floortile_data_id(1))
            data_tuple.append(db.retrieve_floortile_data_id(2))
            data_tuple.append(db.retrieve_floortile_data_id(3))
            data_tuple.append(db.retrieve_floortile_data_id(4))
            for x in data_tuple:
                self.contents.append(FloorTileLeaf(p_db_tuple=x))

            self.floorid = "Ground"
        elif (p_floor == "Upper" or p_floor == "upper"):
            ids = db.retrieve_floortile_id_floorlevel(4, plus_adjacent=True)

            data_tuple.append(db.retrieve_floortile_data_id(5))
            for x in data_tuple:
                self.contents.append(FloorTileLeaf(p_db_tuple=x))

            self.floorid = "Upper"
        else:
            print("INVALID p_floor VALUE (FloorGrid Constructor):  " + str(p_floor))
            self.floorid = "No Floor"

        # Setup self.possible with the id nums retrieved and stored in ids
        self.possible = []
        for x in ids[1:]:
            if self.floorid != "Ground" or x[0] > 4:
                self.possible.append(x[0])

        # Still requires setup_floor_neighbors(p_floorgridlist) to be
        # called to setup self.neighbors before FloorGrid can be used
        db.close()

    def setup_floor_neighbors(self, p_floorgridlist):
        """ Sets up self.neighbors from the passed FloorGrid list """
        #    p_floorgridlist expected index format:
        #    0 = Basement, 1 = Ground, 2 = Upper

        self.neighbors = [None]*2
        if (self.floorid == "Basement"):
            self.neighbors[1] = p_floorgridlist[1]
            self.contents[0].neighbors.add(
                p_floorgridlist[1].contents[3], "Special", 5)
            self.contents[0].doors.append(False)
            self.contents[0].doors.append(True)
        elif (self.floorid == "Ground"):
            self.neighbors[0] = p_floorgridlist[0]
            self.neighbors[1] = p_floorgridlist[2]
            for x in range(4):
                if x-1 >= 0:
                    self.contents[x].neighbors.add(self.contents[x-1], "Right")
                if x+1 < 4:
                    self.contents[x].neighbors.add(self.contents[x+1], "Left")
                if x == 3:
                    self.contents[x].neighbors.add(
                        p_floorgridlist[0].contents[0], "Special", 4)
                    self.contents[x].neighbors.add(
                        p_floorgridlist[2].contents[0], "Special", 5)
                    self.contents[x].doors.append(True)
                    self.contents[x].doors.append(True)
        elif (self.floorid == "Upper"):
            self.neighbors[0] = p_floorgridlist[1]
            self.contents[0].neighbors.add(
                p_floorgridlist[1].contents[3], "Special", 4)
            self.contents[0].doors.append(True)

    def remove_poss_floortile(self, p_id):
        """ Removes p_id from current FloorGrid object and all of it's applicable neighbors """
        self.possible.remove(p_id)
        for x in self.neighbors:
            if x is not None and p_id in x.neighbors:
                x.neighbors.remove(p_id)
