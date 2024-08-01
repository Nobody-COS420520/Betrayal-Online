# pylint: disable=C0301, E0602, W0603
"""  The first file concatted into the final .py that gets run  """
#    pygame zero only works with one module so all .py in /src are
#    concatenated into one single .py module upon docker run/start.
#    THIS IS MULTIPLE FILES CONCATENATED INTO ONE,
#    INDIVIDUAL FILES LOCATED IN /SRC

import pgzrun
import pygame
import math
import collections
import json
import os.path
import random
import sqlite3
import tkinter.messagebox


WIDTH = 1280
HEIGHT = 720
TITLE = "Betrayal Online"
PREV_GAME_STAGE = -1
GAME_STAGE = -1
#   -1 = used to detect when program is first opened (gets changed in first loop of update())
# 0 = program setup (pre main menu)
# 1 = main menu
# 2 = mid game (during an active game)
STAGEOBJ = None			# Holds object for current stage
DBURL = "src/db/betrayal.db"
""" Holds the Character class which holds attributes and methods related to the characters """


class Character():
    """ Holds info about Character's status and posessions in a game """

    num_characters = 0          # Static count of all the Character objects in play
    id = None                   # Holds a unique int identifier for each Instance
    # Holds String defining which affiliation Character obj belongs to
    affiliation = None
    name = ""                   # Holds String containing Character object's name
    # Holds String for which color of character the instance belongs to
    color = ""
    statValues = []             # 2D List of Character's possible stat values
    statIndex = []              # List of current indexes for each of Instance's stat lists
    icon = ""                   # Holds URL to png of character's face icon
    card = ""                   # Holds URL to png of character's stat card
    inventory = None            # Holds instance's inventory object
    current_loc = None          # Holds ref to instance's current FloorTile on the game board
    current_floor = None        # Holds ref to instance's current FloorGrid
    win_check = []              # Holds list of functions which return Bool, all need to be true for affiliation to win
                                # if None instead of [], no checks exist yet and character cannot win
    actor = None                # Holds Actor for Character instance's logo

    def __init__(self, p_db_tuple=None):
        """ Character class constructor """
        self.id = self.num_characters
        self.num_characters += 1
        self.inventory = self.Inventory()
        self.current_loc = None
        self.current_floor = None
        # call instance.assignCharacter(db_tuple) to assign values to the obj's important attributes
        # that's probably the more realistic implementation, this is good for testing
        if p_db_tuple is not None:
            self.assign_character(p_db_tuple)
        self.affiliation = "Explorer"
        self.win_check = []
        

    class Inventory():
        """ Holds a list of a Character object's held items and methods to  """

        def __init__(self):
            self.contents = []

        # Behavior that affects every item in inventory should get a method around here

        def end_of_turn(self):
            """ maybe todo? """
            # Activate every inventory item's end_of_turn behavior if any

    def assign_character(self, p_db_tuple):
        """ Assigns values to a Character object from a Database Tuple.

            Format of p_db_tuple is: 
            (id, name, color, 
            speedValues, speedStartIndex, 
            mightValues, mightStartIndex, 
            sanityValues, sanityStartIndex, 
            knowledgeValues, knowledgeStartIndex, 
            iconURL, cardURL)"""

        self.id = p_db_tuple[0]
        self.name = p_db_tuple[1]
        self.color = p_db_tuple[2]
        x = 3
        self.statValues = []
        self.statIndex = []
        while (x < 10):
            self.statValues.append(json.loads(p_db_tuple[x]))
            self.statIndex.append(p_db_tuple[x+1])
            x += 2
        self.icon = p_db_tuple[11]
        self.card = p_db_tuple[12]

        self.actor = Actor(self.icon)

    def establish_actor(self, p_position, p_width):
        """ Sets up Character actor data in p_gridspace with correct position and scale """
        
        self.actor = Actor(self.icon, topleft=p_position, anchor=(0,0))
        self.actor._surf = pygame.transform.scale(self.actor._surf, (p_width, p_width))
        self.actor._update_pos()

# pylint: disable=C0301
""" Contains CharDBManager class which is used to interact with a Database """


class DBManager():
    """ Holds methods to operate a Database """

    id = "This seems useful but not being used now, only usage is in __init__"
    url = ""                        # Holds url to db file
    conn = None                     # Holds sqlite Connection object

    def __init__(self, p_url, p_id=0):
        self.id = p_id
        self.url = p_url
        self.conn = sqlite3.connect(self.url)

    def create_character_db(self):
        """ Creates Characters table that stores all character's gameplay stats """
        c = self.conn.cursor()
        c.execute("""
                  CREATE TABLE Characters(
                  id INT,
                  Name TEXT,
                  Color TEXT,
                  SpeedValues TEXT,
                  SpeedStartIndex INT,
                  MightValues TEXT,
                  MightStartIndex INT,
                  SanityValues TEXT,
                  SanityStartIndex INT,
                  KnowledgeValues TEXT,
                  KnowledgeStartIndex INT,
                  Icon TEXT,
                  Card TEXT)""")
        c.execute("""INSERT INTO Characters VALUES
                  (0, 'Brandon Jaspers', 'Green', 
                  '[-1,3,4,4,4,5,6,7,8]', 3,
                  '[-1,2,3,3,4,5,6,6,7]', 4,
                  '[-1,3,3,3,4,5,6,7,8]', 4,
                  '[-1,1,3,3,5,5,6,6,7]', 3,
                  'players/icons/bj2.png','players/player_cards/bj.png'),
            
                  (1, 'Darrin \"Flash\" Williams', 'Red', 
                  '[-1,4,4,4,5,6,7,7,8]', 5,
                  '[-1,2,3,3,4,5,6,6,7]', 3,
                  '[-1,1,2,3,4,5,5,5,7]', 3,
                  '[-1,2,3,3,4,5,5,5,7]', 3,
                  'players/icons/dfw2.png','players/player_cards/dfw.png')
                  """)

        self.conn.commit()

    def create_grimoire_db(self):
        """ Creates Grimoire table that includes all character data for the Grimoire mode """
        c = self.conn.cursor()
        c.execute("""CREATE TABLE Grimoire(
                  id INT,
                  Age INT,
                  Height INT,
                  Weight INT,
                  Hobbies TEXT,
                  Description TEXT,
                  Birthday TEXT)
                  """)
        self.conn.commit()

    def create_floortile_db(self):
        """ Creates FloorTile table that includes all character data for the Grimoire mode """
        c = self.conn.cursor()
        # No room logic implemented yet
        # FloorLevels:
        #   0 - Basement ONLY
        #   1 - Basement + Ground Floor
        #   2 - Ground Floor ONLY
        #   3 - Ground Floor + Upper Floor
        #   4 - Upper Floor ONLY
        #   5 - Basement + Upper Floor
        #   6 - Basement + Ground + Upper

        # Doors Index Format:
        #   0 - Up
        #   1 - Left
        #   2 - Right
        #   3 - Down

        c.execute("""CREATE TABLE FloorTile(
                  id INT,
                  Name TEXT,
                  FloorLevel INT,
                  Doors TEXT,
                  Image TEXT
                  )""")
        c.execute("""INSERT INTO FloorTile VALUES
                  (0, 'Basement Landing', 0,'[1, 1, 1, 1]','rooms/b_basement_landing.png'),
                  (1, 'Doorway', 2,'[0, 1, 0, 0]','rooms/g_door.png'),
                  (2, 'Entrance Hall', 2, '[1, 1, 1, 1]','rooms/g_entrance_hall.png'),
                  (3, 'Foyer', 2,'[1, 1, 1, 1]','rooms/g_foyer.png'),
                  (4, 'Grand Staircase', 2, '[0, 0, 1, 0]','rooms/g_grand_staircase.png'),
                  (5, 'Upper Landing', 4, '[1, 1, 1, 1]','rooms/u_upper_landing.png'),
                  (6, 'Underground Lake', 0, '[1, 0, 1, 0]','rooms/basement/b_underground_lake.jpg'),
                  (7, 'Wine Cellar', 0, '[1, 0, 0, 1]','rooms/basement/b_wine_cellar.jpg'),
                  (8, 'Kitchen', 1, '[1, 0, 1, 0]','rooms/ground_basement/gb_kitchen.jpg'),
                  (9, 'Abandoned Room', 1, '[1, 1, 1, 1]','rooms/ground_basement/gb_abandoned_room.jpg'),
                  (10, 'Ballroom', 2, '[1, 1, 1, 1]','rooms/ground/g_ballroom.jpg'),
                  (11, 'Coal Chute', 2, '[1, 0, 0, 0]','rooms/ground/g_coal_chute.jpg'),
                  (12, 'Bloody Room', 3, '[1, 1, 1, 1]','rooms/upper_ground/ug_bloody_room.jpg'),
                  (13, 'Conservatory', 3, '[1, 0, 0, 0]','rooms/upper_ground/ug_conservatory.jpg'),
                  (14, 'Master Bedroom', 4, '[1, 1, 0, 0]','rooms/upper/u_master_bedroom.jpg'),
                  (15, 'Balcony', 4, '[1, 0, 0, 1]','rooms/upper/u_balcony.jpg'),
                  (16, 'Operating Laboratory', 5, '[0, 0, 1, 1]','rooms/upper_basement/ub_operating_lab.jpg'),
                  (17, 'Servants Quarters', 5, '[1, 1, 1, 1]','rooms/upper_basement/ub_servants_quarters.jpg'),
                  (18, 'Creaky Hallway', 6, '[1, 1, 1, 1]','rooms/upper_ground_basement/ugb_creaky_hallway.jpg'),
                  (19, 'Statuary Corridor', 6, '[1, 0, 0, 1]','rooms/upper_ground_basement/ugb_statuary_corridor.jpg')
                  """)

        self.conn.commit()

    def retrieve_character_data(self):
        """ Returns list of Tuples containing Character gameplay data and stats """
        c = self.conn.cursor()
        c.execute("SELECT * FROM Characters")

        return c.fetchall()

    # def retrieve_single_character_data(self, id = -1, name = -1, color = -1):
        # Returns tuple containing Character

    def retrieve_floortile_data_id(self, p_id):
        """ Returns a tuple containing data for the FloorTile belonging to p_id """
        c = self.conn.cursor()
        c.execute("SELECT * FROM FloorTile WHERE id = " + str(p_id))

        return c.fetchone()

    def retrieve_floortile_id_floorlevel(self, p_floorlevel, plus_adjacent=False):
        """ Returns a tuple containing data for the FloorTile belonging to p_floor_num """
        c = self.conn.cursor()
        if (plus_adjacent):
            c.execute("SELECT id FROM FloorTile WHERE FloorLevel >= " + str(p_floorlevel-1) +
                      " AND FloorLevel <= " + str(p_floorlevel+1) + " OR FloorLevel = 6")
        else:
            c.execute(
                "SELECT id FROM FloorTile WHERE FloorLevel = " + str(p_floorlevel))

        return c.fetchall()

    def create_all_db(self):
        """ Creates all the Tables in one function call """
        self.create_character_db()
        self.create_grimoire_db()
        self.create_floortile_db()

    def close(self):
        """ Closes the connection to a sqlite3.connection object """
        self.conn.close()
"""Example Module to Test Things"""
import numpy

def example_func(p_num):
    """Test Function, Returns a String"""
    return str(p_num) + " OK!!!"


def test_example_func():
    """Unit Test for example_func"""
    assert example_func(4) == "4 OK!!"
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
        padding = 0.2    # percent for ONE icon edge's padding

        # split floortile space into ceil(sqrt(n)) columns (num_hori)
        # and ceil(n/ceil(sqrt(n))) rows (num_vert)
        n = len(self.inhabitants)  # for readability
        num_hori = math.ceil(n**(0.5))
        num_vert = math.ceil(n/num_hori)
        # padding_hori and vert are the horizontal and vertical padding 
        # between edge of floortile and inner contents. 
        # they are in decimal percentage format
        padding_hori = 0.215
        padding_hori = padding_hori*self.gridspace.actor.width
        padding_vert = 0.215
        padding_vert = padding_vert*self.gridspace.actor.height
        l_width = (self.gridspace.actor.width-2*padding_hori)//num_hori
        # Might not need l_height due to squares but is here in case things change at some weird point
        l_height = (self.gridspace.actor.height-2*padding_vert)//num_vert

        h_count = 0
        v_count = 0
        for x in self.inhabitants:
            # Setup hori position
            working_x = self.gridspace.actor.x + h_count*l_width + padding_hori
            h_count += 1
            if h_count >= num_hori:
                h_count = 0

            # Setup vert position
            working_y = self.gridspace.actor.y + v_count*l_height + padding_vert
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
""" Holds class definition for menu objects which contain menu object"""
# pylint: disable=C0301, C0305, R0902


class Menu_Tree():
    """ Holds Tree graph holding Menu_Object instances and their relation """

    contents = []

    def __init__(self):
        """ Menu_Tree Constructor """
        self.contents = []

    def add(self, text, rect=Rect((25, 25), (100, 100))):
        """ Appends a new Menu_Object into the Menu_Tree """
        self.contents.append(self.Menu_Object(text, rect))
        return self.contents[len(self.contents)-1]

    def delete(self, text=None, coords=None, menu_object=None):
        """ Searches and deletes Menu_Object from Menu_Tree instance """
        if text is None and coords is None and menu_object is None:
            print(
                "ERROR in Menu_Tree.delete():  No text, coords or menu_object specified")
            return

        working_obj_list = []

        # If specified
        # Then add menu_object to delete list
        if menu_object is not None:
            working_obj_list.append(menu_object)

        # Else if text is specified
        # Then add all menu_objects with matching text to delete list
        elif text is not None:
            for x in self.contents:
                if x.text.text == text:
                    working_obj_list.append(x)

        # Else if coords are specified
        # Then all menu_obj with rects at the passed tuple (x,y) added to delete list
        elif coords is not None:
            for x in self.contents:
                if x.rect.x <= coords[0] and x.rect.x + x.rect.width > coords[0] \
                        and x.rect.y <= coords[1] and x.rect.y + x.rect.height > coords[1]:
                    working_obj_list.append(x)

        # Go through working_obj_list and delete each one from self.contents
        for x in working_obj_list:
            self.contents.remove(x)

    def draw(self):
        """ Draws all Menu Objects in Menu_Tree. Used in main draw() function """
        for x in self.contents:
            # print("In menu_Tree.draw():  " + str(x.text.text) + ", " + str(x.text.bottomright))
            x.draw()

    @staticmethod
    def get_menu_object(p_mainmenu, p_pos):
        """ Returns menu object at a pos tuple """
        for x in p_mainmenu.option_tree.contents:
            if (p_pos[0] > x.rect[0] and p_pos[0] < x.rect[0]+x.rect[2] and
               p_pos[1] > x.rect[1] and p_pos[1] < x.rect[1]+x.rect[3]):
                return x
        return None

    class Menu_Object():
        """ Class for individual Menu_Objects """
        # Holds references to adjacent Menu_Objects, format is [down, up, left, right]
        adjacencies = None
        on_hover = None  # Holds function to be executed on mouseHover
        on_offhover = None  # Holds function to be executed
        on_mouseup = None  # Holds function to be executed on selection
        text = None  # Holds Menu_Object_Text object which holds all info related to text
        rect = ()   # Holds Rect object for selectable area
        highlight_flag = 0  # True if Menu_Object is highlighted

        def __init__(self, text, rect=Rect((25, 25), (100, 100))):
            """ Menu_Object Constructor """
            self.text = Text(text)
            self.on_hover = lambda x: print(x)
            self.on_offhover = lambda x: print(x)
            self.on_mouseup = lambda x: print(x)
            self.adjacencies = [None, None, None, None]
            self.rect = rect
            self.highlight_flag = 0

        def draw(self):
            """ Draws text in Menu_Object """
            self.text.draw()
""" Module containing the GameTurn class and related behavior """


class GameTurn():
    """ Stores information and offers processes for game turn related processes """

    character = None            # Holds ref to character making the turn
    events = []                 # Holds information about events that occured
    # Holds # of moves available for character (initialized to speed stat)
    remaining_moves = 0
    # Integer flag for game_stage for this turn (useful in turn archival)
    game_stage = 0
    # game_stage Format:
    # 0 = exploration phase
    # 1 = pre-haunt phase
    # 2 = haunt phase
    turn_phase = 0              # Integer flag for stage of current turn
    # turn_phase Format:
    # 0 - movement preview
    # 1 - rotation preview
    # 2 - post rotation
    rotate_focus = None         # Holds ref to any placed tile that is being rotated
    move_dir = None             # Holds direction of movement, used in rotating new tiles

    def __init__(self, p_character, game_stage, p_midgame_instance=None):
        """ Constructor for GameTurn class """
        self.character = p_character
        self.events = []
        self.remaining_moves = p_character.statValues[0][p_character.statIndex[0]]
        self.game_stage = game_stage
        self.turn_phase = 0
        self.rotate_focus = None

        self.new_action("Start Turn", turn_phase=self.turn_phase,
                        destination_tile=p_character.current_loc.name, remaining_moves=self.remaining_moves)

        if p_midgame_instance is None:
            stage_instance = STAGEOBJ
        else:
            stage_instance = p_midgame_instance
        stage_instance.display_floorgrid(
            p_character.current_floor, p_character.current_loc)
        stage_instance.floor_index = p_character.current_floor

        # p_foreground_ui is only ment to be passed during constructor of MidGameStage,
        # when STAGEOBJ is still being assigned

        stage_instance.foreground_ui["card"] = Actor(p_character.card, topleft=(
            WIDTH-(WIDTH//4), HEIGHT-(HEIGHT//2.35)))
        stage_instance.foreground_ui["card"]._surf = pygame.transform.scale(
            stage_instance.foreground_ui["card"]._surf, (WIDTH//4, HEIGHT//2.384))
        stage_instance.foreground_ui["card"]._update_pos()
        stage_instance.foreground_ui["next_icon"] = Actor(stage_instance.turn_q[1].icon, topleft=(
            WIDTH-(WIDTH//14.22)-(WIDTH//80), (HEIGHT//72)))
        stage_instance.foreground_ui["next_icon"]._surf = pygame.transform.scale(
            stage_instance.foreground_ui["next_icon"]._surf, (WIDTH//14.22, HEIGHT//8))
        stage_instance.foreground_ui["next_icon"]._update_pos()
        # Old lines of code, retained in order to have an older version available to fall back to
        #stage_instance.foreground_ui["next_icon"]._surf, (WIDTH//21.36, HEIGHT//12.024))
        #stage_instance.foreground_ui["next_icon"].topleft = (WIDTH-(WIDTH//25.6), (HEIGHT//72))
        stage_instance.option_tree.delete(
            coords=((WIDTH//1.268), (HEIGHT//6.0674)))
        working_menu_obj = stage_instance.option_tree.add(str(self.remaining_moves), Rect(
            (WIDTH-(WIDTH//4.9)-(WIDTH//14.55), HEIGHT//10), (WIDTH//14.55, HEIGHT//7)))
        working_menu_obj.text.midgame_default(working_menu_obj)
        working_menu_obj.text.fontname = "butcherman-regular.ttf"
        working_menu_obj.text.fontsize = 82*(HEIGHT/1080)
        working_menu_obj.on_hover = lambda x: 1
        working_menu_obj.on_offhover = lambda x: 1
        working_menu_obj.text.color = "#ddc94e"
        working_menu_obj.text.bottomright = working_menu_obj.rect.bottomright

    def turn_start(self, p_func_list):
        """ Executes list of functions holding logic to be executed first in turn """

    # def turn_end(self, p_func_list):
    #    """ Executes list of functions holding logic to be executed first in turn """

    def move(self, p_direction, p_special=None):
        """ Adds move preview event to the event list """

        # If turn_phase is not in movement stage
        # Then return without doing anything
        if self.turn_phase != 0:
            return

        # Switch p_direction from String to index to be used with adjacency arrays
        if p_direction == "Up" or p_direction == "up":
            p_direction = 0
        elif p_direction == "Left" or p_direction == "left":
            p_direction = 1
        elif p_direction == "Right" or p_direction == "right":
            p_direction = 2
        elif p_direction == "Down" or p_direction == "down":
            p_direction = 3
        elif (p_direction == "Special" or p_direction == "special") and p_special is not None:
            p_direction = p_special
            if p_special >= len(self.character.current_loc.neighbors.neighbors):
                print("ERROR in GameTurn.move():  p_special out of bounds for current FloorTile:  " +
                      str(self.character.current_loc.name) + ", " + str(p_direction))
                return -1

        v_start = self.character.current_loc
        opp_direction = STAGEOBJ.opp_direction(p_direction)

        # If there is a doorway in the direction of move
        # Then check if destination has a tile
        # print("BEGINNING MOVE")

        #if v_start.doors[p_direction] and v_start.neighbors.neighbors[p_direction] is not None:
        if v_start.doors[p_direction]:

            v_dest = v_start.neighbors.neighbors[p_direction]

            # If v_dest does not have a tile and there are still moves remaining
            # Then draw a tile, create an event and begin rotation phase
            if v_dest is None and self.remaining_moves > 0 and p_direction < 4:
                # print("V_DEST IS UNDISCOVERED")
                v_dest = STAGEOBJ.draw_floortile(
                    v_start.gridspace.neighbors[p_direction])
                v_start.neighbors.neighbors[p_direction] = v_dest
                self.rotate_focus = v_dest
                self.move_dir = p_direction
                self.rotate_focus_by_doors(force_rotate=False)
                self.new_action("Place New Tile", new_tile=v_dest.name)
                self.turn_phase = 1     # Begin Rotation Phase
                return self

            # If tile in destination exists in the event list as a preview before any rollback_stops,
            # Then delete all non-stop events that occured after the movement preview
            # will contain strings of action_descriptions
            rollback_stops = ["Finalize Rotation"]
            for x in range(len(self.events)-1, -1, -1):
                if self.events[x].action_description in rollback_stops:
                    break
                if self.events[x].data_dict["destination_tile"] is not None and \
                        v_dest is not None and v_dest.doors[opp_direction] == True and self.events[x].data_dict["destination_tile"] == v_dest.name:

                    if p_direction == 4:
                        # print("DOWN FLOOR")
                        STAGEOBJ.floor_index -= 1
                    if p_direction == 5:
                        # print("UP FLOOR")
                        STAGEOBJ.floor_index += 1
                    STAGEOBJ.display_floorgrid(STAGEOBJ.floor_index, v_dest)
                    self.character.current_floor = STAGEOBJ.floor_index
                    self.update_remaining_moves(
                        self.events[x].data_dict["remaining_moves"])
                    STAGEOBJ.place_character(self.character, v_dest)
                    self.events = self.events[:x+1]
                    return self

            # If destination has a tile and there are still moves remaining
            # Then wrap up successful move and create event
            # else draw, move and begin rotation phase
            if v_dest and v_dest.doors[opp_direction] == True and self.remaining_moves > 0:
                # print("NEW TILE")
                if p_direction == 4:
                    # print("DOWN FLOOR")
                    STAGEOBJ.floor_index -= 1
                if p_direction == 5:
                    # print("UP FLOOR")
                    STAGEOBJ.floor_index += 1
                STAGEOBJ.display_floorgrid(STAGEOBJ.floor_index, v_dest)
                self.character.current_floor = STAGEOBJ.floor_index

                self.update_remaining_moves(self.remaining_moves-1)
                STAGEOBJ.place_character(self.character, v_dest)
                self.new_action("Movement Preview", destination_tile=v_dest.name,
                                remaining_moves=self.remaining_moves)
                return self

    def rotate_focus_by_doors(self, p_rotate_dir="Left", force_rotate=True):
        """ Rotates p_dest_tile so its doors are aligned with p_start_tile's doors. """

        num_rotates = 0
        # pylint: disable-next=C0121
        while self.rotate_focus.doors[STAGEOBJ.opp_direction(self.move_dir)] != 1 or force_rotate == True:
            num_rotates += 1
            self.rotate_focus.rotate_doors(p_rotate_dir)
            force_rotate = False
        STAGEOBJ.rotate(p_rotate_dir, self.rotate_focus.gridspace,
                        num_rotates=num_rotates)

    def finalize_rotation(self):
        """ Executes logic to finalize the Rotation Phase (self.turn_phase == 1) """
        self.new_action("Finalize Rotation", angle=self.rotate_focus.angle)
        STAGEOBJ.place_character(self.character, self.rotate_focus)
        STAGEOBJ.display_floorgrid(STAGEOBJ.floor_index, self.rotate_focus)
        self.update_remaining_moves(0)
        self.turn_phase = 2  # Post Rotation Phase

        # Setting up self.rotate_focus' neighbors and setting it as neighbor's neighbor
        f = self.rotate_focus
        for x in range(4):
            f.neighbors.neighbors[x] = f.gridspace.neighbors[x].floortile
            if f.gridspace.neighbors[x].floortile is not None:
                f.neighbors.neighbors[x].neighbors.neighbors[STAGEOBJ.opp_direction(
                    x)] = f

    def wrap_up_turn(self):
        """ Executes logic to end a turn """
        if self.turn_phase == 1:
            self.finalize_rotation()
        self.new_action("End Turn", final_tile=self.character.current_loc.name)
        win = False
        for x in self.character.win_check:
            x()

    def update_remaining_moves(self, p_moves):
        """ Updates everything that needs to be updated upon change of self.remaining_moves """
        working_obj = Menu_Tree.get_menu_object(
            STAGEOBJ, (WIDTH//1.27, HEIGHT//6.467))
        working_obj.text.text = str(p_moves)
        self.remaining_moves = p_moves

    def new_action(self, p_action_description, **kwargs):
        """ Creates new Action obj and appends into self.events """
        self.events.append(self.Action(p_action_description, **kwargs))

    class Action():
        """ Contains data for actions that can occur during a turn """

        action_description = ""         # Holds String defining what action occured
        # Holds Dictionary containing all data passed to constructor in **kwargs
        data_dict = None

        def __init__(self, p_action_description, **kwargs):
            self.action_description = p_action_description
            self.data_dict = kwargs

        def __repr__(self):
            working_string = str(self.action_description) + \
                ":  " + str(self.data_dict)
            return working_string
""" Holds Text class which holds all instance data needed for pygame zero text """


class Text():
    """ Holds all instance data needed for pygame zero text """
    text = ""  # Holds the text of a Menu_object
    fontname = "Calibri"  # Holds fontname of Menu_object's text
    fontsize = 24  # Holds fontsize of Menu_object's text
    antialias = True  # Flag for text to be rendered with antialias, default is True
    color = "white"  # Holds color of text
    background = None  # Holds background color for text to use

    top = None  # Positional variables
    left = None
    bottom = None
    right = None
    topleft = None
    bottomleft = None
    topright = None
    bottomright = None
    midtop = None
    midleft = None
    midbottom = None
    midright = None
    center = None
    centerx = None
    centery = None

    width = None  # Holds width of text for formatting
    widthem = None  # Holds width of text in em
    lineheight = 1.0  # Holds vertical spacing between lines in units of font's default height
    #   Can prevent line wrapping by including non-breaking space chars: \u00A0

    align = None  # Holds horizontal positioning of text

    owidth = None  # Holds outline width in outline units
    ocolor = "black"  # Holds outline color

    # Holds (x,y) values representing the drop shadow offset in shadow units
    shadow = None
    scolor = "black"  # Holds drop shadow color

    gcolor = None  # Holds lower gradient stop color

    alpha = 1.0  # Holds alpha transparency, range from 0.0-1.0

    anchor = (0.0, 0.0)  # Holds anchor position, range from 0.0-1.0

    angle = 0  # Holds counterclockwise rotational value in deg
    #   Pygame Zero rounds to nearest multiple of 3 deg

    highlight_color = "black"

    def __init__(self, text, fontname="Calibri", fontsize=24, antialias=True,
                 color="white", background=None, top=None, left=None,
                 bottom=None, right=None, topleft=None, bottomleft=None,
                 topright=None, bottomright=None, midtop=None, midleft=None,
                 midbottom=None, midright=None, center=None, centerx=None,
                 centery=None, width=None, widthem=None, lineheight=1.0,
                 align=None, owidth=None, ocolor="black", shadow=None,
                 scolor="black", gcolor=None, alpha=1.0, anchor=(0.0, 0.0),
                 angle=0, highlight_color="black"):
        self.text = text
        self.fontname = fontname
        self.fontsize = fontsize
        self.antialias = antialias
        self.color = color
        self.background = background
        self.top = top
        self.left = left
        self.bottom = bottom
        self.right = right
        self.topleft = topleft
        self.bottomleft = bottomleft
        self.topright = topright
        self.bottomright = bottomright
        self.midtop = midtop
        self.midleft = midleft
        self.midbottom = midbottom
        self.midright = midright
        self.center = center
        self.centerx = centerx
        self.centery = centery
        self.width = width
        self.widthem = widthem
        self.lineheight = lineheight
        self.align = align
        self.owidth = owidth
        self.ocolor = ocolor
        self.shadow = shadow
        self.scolor = scolor
        self.gcolor = gcolor
        self.alpha = alpha
        self.anchor = anchor
        self.angle = angle
        self.highlight_color = highlight_color

    def draw(self):
        """ Draws a text item. Used in main draw() function """
        screen.draw.text(self.text, fontname=self.fontname, fontsize=self.fontsize,
                         antialias=self.antialias, color=self.color,
                         background=self.background, top=self.top, left=self.left,
                         bottom=self.bottom, right=self.right, topleft=self.topleft,
                         bottomleft=self.bottomleft, topright=self.topright,
                         bottomright=self.bottomright, midtop=self.midtop, midleft=self.midleft,
                         midbottom=self.midbottom, midright=self.midright, center=self.center,
                         centerx=self.centerx, centery=self.centery, width=self.width,
                         widthem=self.widthem, lineheight=self.lineheight, align=self.align,
                         owidth=self.owidth, ocolor=self.ocolor, shadow=self.shadow, scolor=self.scolor,
                         gcolor=self.gcolor, alpha=self.alpha, anchor=self.anchor, angle=self.angle)

    def midgame_default(self, p_menu_obj, p_fontsize = 52):
        """ Sets Text obj to default settings for the MidGame stage """
        self.color = "#f27b00"
        self.fontname = "lastman.ttf"
        self.fontsize = p_fontsize
        self.ocolor = "white"
        self.owidth = 500  # not working
        self.shadow = (0, 1)
        self.scolor = "#443f12" #
        self.highlight_color =  "#443f32"#"black"
        p_menu_obj.on_hover = Midgame.on_hover
        p_menu_obj.on_offhover = Midgame.on_offhover
        p_menu_obj.on_mouseup = Midgame.on_mouseup
"""Holds functions related to the mainmenu Game Stage"""


class MainMenu():
    """ Singleton class holding properties of the mainmenu Game Stage (stage number 1) """

    actors = None  # Holds list of Actor objects for main menu
    option_tree = None  # Holds tree vector for each menu item
    #   each index is a list of indexes representing adjacencies
    #   format is [down, up, left, right]

    def __init__(self):
        """ MainMenu class constructor """
        self.actors = []
        self.actors.append(Actor("bo_specific/main-menu-bg-1920x1080.png", topleft=(0,0), anchor=(0,0)))
        self.actors[0]._surf = pygame.transform.scale(self.actors[0]._surf, (WIDTH, HEIGHT))
        self.actors[0]._update_pos()
        
        self.actors.append(Actor("bo_specific/betrayal_logo_transparent_1920x1080.png",
                           topleft=(WIDTH*0.284, HEIGHT*0.05238)))
    #WIDTH*0.48
        self.actors[1]._surf = pygame.transform.scale(self.actors[1]._surf, (WIDTH*0.39, HEIGHT*0.19))
        self.actors[1]._update_pos()

        self.option_tree = Menu_Tree()

        self.option_tree.add("ONLINE", rect=Rect(
            (int(WIDTH/2.19), int(HEIGHT/2.2)), (int(WIDTH/11.64), int(HEIGHT/13.5))))
        self.option_tree.add("LOCAL VS", rect=Rect(
            (int(WIDTH/2.29), int(HEIGHT/1.86)), (int(WIDTH/8.17), int(HEIGHT/13.5))))
        self.option_tree.add("GRIMOIRE", rect=Rect(
            (int(WIDTH/2.29), int(HEIGHT/1.61)), (int(WIDTH/8.17), int(HEIGHT/13.5))))
        self.option_tree.add("SETTINGS", rect=Rect(
            (int(WIDTH/2.27), int(HEIGHT/1.42)), (int(WIDTH/8.53), int(HEIGHT/13.5))))
        self.option_tree.add("EXIT", rect=Rect(
            (int(WIDTH/2.13), int(HEIGHT/1.27)), (int(WIDTH/16.7), int(HEIGHT/13.5))))

        incrementing_height = HEIGHT/2
        for x in self.option_tree.contents:
            x.text.center = (WIDTH/2, incrementing_height)
            x.text.color = "#ddc94e"
            x.text.fontname = "lastman.ttf"
            x.text.fontsize = 64*(HEIGHT/1080)      # 64 is default font for a screen height of 1080, this line scales the text to window height
            x.text.ocolor = "white"
            x.text.owidth = 500  # not working
            x.text.shadow = (0, 1)
            x.text.scolor = "#443f12"
            x.text.highlight_color = "#443f32"
            x.on_hover = MainMenu.on_hover
            x.on_offhover = MainMenu.on_offhover
            x.on_mouseup = MainMenu.on_mouseup
            # x.on_mouseup = self.
            incrementing_height += HEIGHT/12

        self.option_tree.contents[0].on_mouseup = MainMenu.online_mouseup

        #   setting up menu option tree adjacencies
        self.option_tree.contents[0].adjacencies = [self.option_tree.contents[1],
                                                    self.option_tree.contents[len(self.option_tree.contents)-1], None, None]
        for x in range(1, len(self.option_tree.contents)-1):
            self.option_tree.contents[x].adjacencies = [
                self.option_tree.contents[x+1], self.option_tree.contents[x-1], None, None]
        self.option_tree.contents[len(self.option_tree.contents)-1].adjacencies = [
            self.option_tree.contents[0], self.option_tree.contents[len(self.option_tree.contents)-2], None, None]

    @staticmethod
    def on_hover(p_menu_object):
        """ Executes on hover over MainMenu menu object """
        p_menu_object.text.fontsize = 82*(HEIGHT/1080)

    @staticmethod
    def on_offhover(p_menu_object):
        """ Executes on offhover over MainMenu menu object """
        p_menu_object.text.fontsize = 64*(HEIGHT/1080)
        p_menu_object.highlight_flag = 0

    @staticmethod
    def on_mouseup(p_menu_object):
        """ Executes on hover over MainMenu menu object """
        p_menu_object.highlight_flag = 1

    @staticmethod
    def online_mouseup(p_menu_object):
        """ Goes into GAME_STAGE 2 (Midgame) when 'ONLINE' gets pressed """
        global GAME_STAGE
        GAME_STAGE = 2
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
"""Main Module for Betrayal at the House on the Hill by Nobody"""


def on_mouse_move(pos, rel, buttons):
    """    
        pos = tuple (x,y) that gives location that the mouse pointer moved to
        rel = tuple (delta_x, delta_y) that represents the change in the mouse pointer's position
        buttons = set of mouse enum values indicating the buttons that were down during the moved
    """
    global GAME_STAGE

    print("mouse move:  " + str(pos) + "  " + str(rel) + "  " + str(buttons))

    match(GAME_STAGE):
        case 1:     # MainMenu stage
            prev = Menu_Tree.get_menu_object(
                STAGEOBJ, (pos[0]-rel[0], pos[1]-rel[1]))
            current = Menu_Tree.get_menu_object(STAGEOBJ, pos)
            if current != prev:
                if current is not None:
                    current.on_hover(current)
                if prev is not None:
                    prev.on_offhover(prev)
        case 2:     # Midgame stage
            prev_isgrid = False
            current_isgrid = False
            # If mouse on/off of MenuObject
            # Then set current/prev to MneuObject
            # Else check if mouse on/off GridSpace
            prev = Menu_Tree.get_menu_object(
                STAGEOBJ, (pos[0]-rel[0], pos[1]-rel[1]))
            if prev is not None:
                prev.on_offhover(prev)
            else:
                prev = STAGEOBJ.get_grid_loc((pos[0]-rel[0], pos[1]-rel[1]))
                prev_isgrid = True
            current = Menu_Tree.get_menu_object(STAGEOBJ, pos)
            if current is not None:
                current.on_hover(current)
            else:
                current = STAGEOBJ.get_grid_loc(pos)
                current_isgrid = True
            if current != prev:
                #   validity check if current is in the range of possible Midgame.grid squares
                if current_isgrid and current[0] < len(STAGEOBJ.grid) and current[1] < len(STAGEOBJ.grid[0]):
                    # Midgame.grid[current[0]][current[1]].on_hover(current[0], current[1])
                    STAGEOBJ.grid[current[0]][current[1]].on_hover()
                #   this validity check is necessary if mouse is reentering grid from outside
                if prev_isgrid and prev[0] < len(STAGEOBJ.grid) and prev[1] < len(STAGEOBJ.grid[0]):
                    STAGEOBJ.grid[prev[0]][prev[1]].on_offhover()


def on_mouse_down(pos, button):
    """
        pos = tuple (x,y) that gives location of the mouse pointer when the button was pressed
        button = mouse enum value indicating which button was pressed
    """
    global GAME_STAGE

    print("mouse down:  " + str(pos) + "  " + str(button))

    match(GAME_STAGE):
        case 1:  # MainMenu Stage
            pass
        case 2:  # Midgame Stage
            current = STAGEOBJ.get_grid_loc(pos)
            #   validity check if left mousebutton and current is in the range of possible Midgame.grid squares
            if button == 1 and current[0] < len(STAGEOBJ.grid) and current[1] < len(STAGEOBJ.grid[0]):
                STAGEOBJ.grid[current[0]][current[1]].on_mousedown(
                    current[0], current[1])


def on_mouse_up(pos, button):
    """
        pos = tuple (x,y) that gives location of the mouse pointer when the button was released
        button = mouse enum value indicating the button that was released
    """
    global GAME_STAGE

    print("mouse up:  " + str(pos) + "  " + str(button))

    match(GAME_STAGE):
        case 1:                             # MainMenu Stage
            if button == 1:
                current = Menu_Tree.get_menu_object(STAGEOBJ, pos)
                if current is not None:
                    current.on_mouseup(current)
            pass
        case 2:  # Midgame Stage
            if button == 1:
                # If user clicks on a menu object
                # Then do only menu_object.on_mouseup()
                # Else, do GridSpace.on_mouseup()
                current = Menu_Tree.get_menu_object(STAGEOBJ, pos)
                if current is not None:
                    current.on_mouseup(current)
                else:
                    current = STAGEOBJ.get_grid_loc(pos)
                    #   validity check if left mousebutton and current is in the range of possible GRID squares
                    if current[0] < len(STAGEOBJ.grid) and current[1] < len(STAGEOBJ.grid[0]):
                        STAGEOBJ.grid[current[0]][current[1]].on_mouseup(
                            current[0], current[1])


def on_key_down(key, mod, unicode):
    """
        key = integer indicating the key that was pressed
        mod = bitmask of modifier keys that are down
        unicode = the character that was typed *includes control characters?*
                *Will return empty string if key doesn't correspond to a Unicode char
    """

    global GAME_STAGE

    print("key down:  " + str(key) + "  " + unicode)

    match(GAME_STAGE):
        case 1:                     # mainmenu stage
            pass
        case 2:                     # midgame stage
            match(key):
                case 1073741921:    # numpad 9
                    STAGEOBJ.zoom(1.25)
                case 1073741920:    # numpad 8
                    STAGEOBJ.cam_move_vert(150)
                case 1073741919:    # numpad 7
                    STAGEOBJ.zoom(0.8)
                case 1073741918:    # numpad 6
                    STAGEOBJ.cam_move_hori(-150)
                case 1073741916:    # numpad 4
                    STAGEOBJ.cam_move_hori(150)
                case 1073741915:    # numpad 3
                    if (STAGEOBJ.floor_index+1 < 3):
                        STAGEOBJ.display_floorgrid(STAGEOBJ.floor_index+1)
                        STAGEOBJ.floor_index += 1
                case 1073741914:    # numpad 2
                    STAGEOBJ.cam_move_vert(-150)
                case 1073741913:    # numpad 1
                    if (STAGEOBJ.floor_index-1 >= 0):
                        STAGEOBJ.display_floorgrid(STAGEOBJ.floor_index-1)
                        STAGEOBJ.floor_index -= 1


def on_key_up(key, mod):
    """
        key = integer indicating the key that was released
        mod = bitmask of modifier keys that are down
    """
    global GAME_STAGE

    print("key up:  " + str(key) + "  " + str(mod))

    match(GAME_STAGE):
        case 1:                     # MainMenu Stage
            match(key):
                case 119:           # w
                    match(mod):
                        case 4097:  # left shift
                            GAME_STAGE = 2
                case 122:           # Z
                    match(mod):
                        case 4097:  # left shift
                            GAME_STAGE = 0
        case 2:                     # Midgame Stage
            match(key):
                case 13:            # Enter key
                    match(mod):
                        case default:
                            turn = STAGEOBJ.turn[len(STAGEOBJ.turn)-1]
                            if turn.turn_phase == 1:
                                turn.finalize_rotation()
                case 113:           # Q
                    match(mod):
                        case 4097:  # left shift
                            GAME_STAGE = 1
                case 119:           # w
                    match(mod):
                        case 4097:  # left shift
                            # reset midgame stage
                            STAGEOBJ.setup_midgame()
                case 122:           # Z
                    match(mod):
                        case 4097:  # left shift
                            GAME_STAGE = 0
                case 1073741906:    # Up Arrow
                    match(mod):
                        case 4097:  # left shift
                            turn = STAGEOBJ.turn[len(STAGEOBJ.turn)-1]
                            if turn.turn_phase == 0:    # Movement Phase
                                turn.move("Special", 5)
                        case default:
                            turn = STAGEOBJ.turn[len(STAGEOBJ.turn)-1]
                            if turn.turn_phase == 0:    # Movement Phase
                                turn.move("Up")
                case 1073741904:    # Left Arrow
                    match(mod):
                        case default:
                            turn = STAGEOBJ.turn[len(STAGEOBJ.turn)-1]
                            if turn.turn_phase == 0:    # Movement Phase
                                turn.move("Left")
                            elif turn.turn_phase == 1:
                                turn.rotate_focus_by_doors("Left")
                case 1073741903:    # RIGHT Arrow
                    match(mod):
                        case default:
                            turn = STAGEOBJ.turn[len(STAGEOBJ.turn)-1]
                            if turn.turn_phase == 0:    # Movement Phase
                                turn.move("Right")
                            elif turn.turn_phase == 1:
                                turn.rotate_focus_by_doors("Right")
                case 1073741905:    # Down Arrow
                    match(mod):
                        case 4097:  # left shift
                            turn = STAGEOBJ.turn[len(STAGEOBJ.turn)-1]
                            if turn.turn_phase == 0:    # Movement Phase
                                turn.move("Special", 4)
                        case default:
                            turn = STAGEOBJ.turn[len(STAGEOBJ.turn)-1]
                            if turn.turn_phase == 0:    # Movement Phase
                                turn.move("Down")

        case default:               # no game stage
            match(key):
                case 113:           # Q
                    match(mod):
                        case default:
                            # enter mainmenu stage
                            GAME_STAGE = 1
                case 119:           # W
                    match(mod):
                        case default:
                            # enter midgame stage
                            GAME_STAGE = 2


def update(time_elapsed):
    """
        time_elapsed = time in ms since previous call to update()
    """

    global GAME_STAGE
    global PREV_GAME_STAGE
    global STAGEOBJ

    # On program start: set GAME_STAGE to 1 (MainMenu)
    # Also check if this is first time opening and create everything important
    if GAME_STAGE == -1:
        GAME_STAGE = 1
        if (not os.path.exists(DBURL)):
            print("Conditional is True")
            os.mkdir(os.path.join("./src", "db"))
            db = DBManager(DBURL)
            db.create_all_db()
            db.close()
            db = None

    # temporary, made to go directly into specific stage
    # GAME_STAGE = 2

    #   Detects whenever game_stage changes (used for game_stage setup)
    #   NEW STAGE SWITCH
    if (GAME_STAGE != PREV_GAME_STAGE):
        match GAME_STAGE:
            case 1:
                STAGEOBJ = MainMenu()
            case 2:
                print("\n" + "going into midgame" + "\n")
                STAGEOBJ = Midgame()
    #   setting up pre_game_stage to be used to detect changes to game_stage
    PREV_GAME_STAGE = GAME_STAGE


def draw():
    """ 
        Gets called automatically whenever something needs to be redrawn.
        Include all of the .draw() methods in here
    """

    global GAME_STAGE
    global GRID

    screen.clear()

    match GAME_STAGE:
        case 1:  # case: main_menu
            if (STAGEOBJ is not None and STAGEOBJ.actors is not None):
                for x in STAGEOBJ.actors:
                    x.draw()
                STAGEOBJ.option_tree.draw()
                for x in STAGEOBJ.option_tree.contents:
                    if x.highlight_flag != 1:
                        screen.draw.rect(x.rect, (255, 0, 0))
                    else:
                        screen.draw.rect(x.rect, x.text.highlight_color)
        case 2:  # case: midgame
            STAGEOBJ.midgame_bg.draw()
            if STAGEOBJ.grid:
                # pylint: disable-next=C0200
                for x in range(len(STAGEOBJ.grid)):
                    for y in range(len(STAGEOBJ.grid[x])):
                        if STAGEOBJ.grid[x][y].actor is not None:
                            STAGEOBJ.grid[x][y].actor.draw()
                        elif STAGEOBJ.grid[x][y].highlight_flag != 1:
                            screen.draw.rect(
                                STAGEOBJ.grid[x][y].rect, (255, 0, 0))
                        else:
                            screen.draw.rect(
                                STAGEOBJ.grid[x][y].rect, STAGEOBJ.grid[x][y].highlight_color)
            for x in STAGEOBJ.turn_q:
                if x.current_floor == STAGEOBJ.floor_index:
                    x.actor.draw()
            STAGEOBJ.option_tree.draw()
            """for x in STAGEOBJ.option_tree.contents:
                if x.highlight_flag != 1:
                    screen.draw.rect(x.rect, (255, 0, 0))
                else:
                    screen.draw.rect(x.rect, x.text.highlight_color)"""
            for x in STAGEOBJ.foreground_ui:
                STAGEOBJ.foreground_ui[x].draw()


pgzrun.go()
