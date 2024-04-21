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

