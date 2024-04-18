""" Module containing the GameTurn class and related behavior """

class GameTurn():
    """ Stores information and offers processes for game turn related processes """

    character = None            # Holds ref to character making the turn
    events = []                 # Holds information about events that occured 
    remaining_moves = 0         # Holds # of moves available for character (initialized to speed stat)
    moves_menu_object = None    # Holds MenuObject instance for # moves left UI element

    def __init__(self, p_character, p_midgame_instance = None):
        """ Constructor for GameTurn class """
        self.character = p_character
        self.events = []
        self.new_action("Start Turn", starting_tile = p_character.current_loc)
        self.remaining_moves = p_character.statValues[0][p_character.statIndex[0]]
        print("In GameTurn init:  " + str(self.remaining_moves))
        #self.moves_menu_object = Menu_
        # p_foreground_ui is only ment to be passed during constructor of MidGameStage,
        # when STAGEOBJ is still being assigned
        if p_midgame_instance is None:
            stage_instance = STAGEOBJ
        else:
            stage_instance = p_midgame_instance
        stage_instance.foreground_ui["card"] = Actor(p_character.card, bottomright=(WIDTH-(WIDTH//120),HEIGHT-(HEIGHT//90)), anchor=("right","bottom"))
        stage_instance.foreground_ui["card"]._surf = pygame.transform.scale(stage_instance.foreground_ui["card"]._surf, (WIDTH//4, HEIGHT//2.384))
        stage_instance.foreground_ui["card"]._update_pos()
        stage_instance.foreground_ui["next_icon"] = Actor(stage_instance.turn_q[1].icon, topright = (WIDTH+(WIDTH//23.4), -1*(HEIGHT//72)), anchor=("right", "top"))
        stage_instance.foreground_ui["next_icon"]._surf = pygame.transform.scale(stage_instance.foreground_ui["next_icon"]._surf, (WIDTH//12.3, HEIGHT//6.9))
        stage_instance.foreground_ui["next_icon"]._update_pos()
        #else:
        #    p_midgame_instance.foreground_ui["card"] = Actor(p_character.card, bottomright=(WIDTH-(WIDTH//120),HEIGHT-(HEIGHT//90)), anchor=("right","bottom"))
        #    p_midgame_instance.foreground_ui["card"]._surf = pygame.transform.scale(p_midgame_instance.foreground_ui["card"]._surf, (WIDTH//4, HEIGHT//2.384))
        #    p_midgame_instance.foreground_ui["card"]._update_pos()
        #    p_midgame_instance.foreground_ui["next_icon"] = Actor(p_midgame_instance.turn_q[1].icon, topright = (WIDTH+(WIDTH//23.4), -1*(HEIGHT//72)), anchor=("right", "top"))
        #    p_midgame_instance.foreground_ui["next_icon"]._surf = pygame.transform.scale(p_midgame_instance.foreground_ui["next_icon"]._surf, (WIDTH//12.3, HEIGHT//6.9))
        #    p_midgame_instance.foreground_ui["next_icon"]._update_pos()


    def turn_start(self, p_func_list):
        """ Executes list of functions holding logic to be executed first in turn """

    def move(self, p_floortile):
        pass
        
    def new_action(self, p_action_description, **kwargs):
        """ Creates new Action obj and appends into self.events """
        self.events.append(self.Action(p_action_description, **kwargs))
        
    class Action():
        """ Contains data for actions that can occur during a turn """

        action_description = ""         # Holds String defining what action occured
        data_dict = None                # Holds Dictionary containing all data passed to constructor in **kwargs

        def __init__(self, p_action_description, **kwargs):
            self.action_description = p_action_description
            self.data_dict = kwargs

        def __repr__(self):
            working_string = str(self.action_description) + ":  " + str(self.data_dict)
            return working_string
    
