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
