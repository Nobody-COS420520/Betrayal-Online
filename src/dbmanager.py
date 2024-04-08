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
                  'images/players/icons/BJ2.png','images/players/player_cards/BJ.png')
                  """)
        c.execute("""INSERT INTO Characters VALUES
                  (1, 'Darrin \"Flash\" Williams', 'Red', 
                  '[-1,4,4,4,5,6,7,7,8]', 5,
                  '[-1,2,3,3,4,5,6,6,7]', 3,
                  '[-1,1,2,3,4,5,5,5,7]', 3,
                  '[-1,2,3,3,4,5,5,5,7]', 3,
                  'images/players/icons/DFW2.png','images/players/player_cards/DFW.png')
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

    #def create_floortile_db(self):
    #    """ Creates FloorTile table that includes all character data for the Grimoire mode """
    #    c = self.conn.cursor()
    #    c.execute("""CREATE TABLE FloorTile(
    #              )
    #              """)
    #    self.conn.commit()

    def retrieve_character_data(self):
        """ Returns list of Tuples containing Character gameplay data and stats """
        c = self.conn.cursor()
        c.execute("SELECT * FROM Characters")

        return c.fetchall()

    def create_all_db(self):
        """ Creates all the Tables in one function call """
        self.create_character_db()
        self.create_grimoire_db()

    def close(self):
        """ Closes the connection to a sqlite3.connection object """
        self.conn.close()
