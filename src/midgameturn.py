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
    turn_stage = 0              # Integer flag for stage of current turn
    # turn_stage Format:
    # 0 - movement preview
    # 1 - rotation preview

    def __init__(self, p_character, game_stage, p_midgame_instance=None):
        """ Constructor for GameTurn class """
        self.character = p_character
        self.events = []
        self.remaining_moves = p_character.statValues[0][p_character.statIndex[0]]
        print("In GameTurn init:  " + str(self.remaining_moves))
        self.game_stage = game_stage
        self.turn_stage = 0
        self.new_action("Start Turn", turn_stage=self.turn_stage,
                        starting_tile=p_character.current_loc)

        # p_foreground_ui is only ment to be passed during constructor of MidGameStage,
        # when STAGEOBJ is still being assigned
        if p_midgame_instance is None:
            stage_instance = STAGEOBJ
        else:
            stage_instance = p_midgame_instance
        stage_instance.foreground_ui["card"] = Actor(p_character.card, bottomright=(
            WIDTH-(WIDTH//120), HEIGHT-(HEIGHT//90)), anchor=("right", "bottom"))
        stage_instance.foreground_ui["card"]._surf = pygame.transform.scale(
            stage_instance.foreground_ui["card"]._surf, (WIDTH//4, HEIGHT//2.384))
        stage_instance.foreground_ui["card"]._update_pos()
        stage_instance.foreground_ui["next_icon"] = Actor(stage_instance.turn_q[1].icon, topright=(
            WIDTH+(WIDTH//23.4), -1*(HEIGHT//72)), anchor=("right", "top"))
        stage_instance.foreground_ui["next_icon"]._surf = pygame.transform.scale(
            stage_instance.foreground_ui["next_icon"]._surf, (WIDTH//12.3, HEIGHT//6.9))
        stage_instance.foreground_ui["next_icon"]._update_pos()
        stage_instance.option_tree.delete(
            coords=((WIDTH//1.268), (HEIGHT//6.0674)))
        working_menu_obj = stage_instance.option_tree.add(str(self.remaining_moves), Rect(
            (WIDTH-(WIDTH//4.9)-(WIDTH//14.55), HEIGHT//10), (WIDTH//14.55, HEIGHT//7)))
        working_menu_obj.text.midgame_default(working_menu_obj)
        working_menu_obj.text.fontname = "butcherman-regular.ttf"
        working_menu_obj.text.fontsize = 82
        working_menu_obj.on_hover = lambda x: 1
        working_menu_obj.on_offhover = lambda x: 1
        working_menu_obj.text.color = "#ddc94e"
        working_menu_obj.text.bottomright = working_menu_obj.rect.bottomright

    def turn_start(self, p_func_list):
        """ Executes list of functions holding logic to be executed first in turn """

    def turn_end(self, p_func_list):
        """ Executes list of functions holding logic to be executed first in turn """

    def move(self, p_floortile):
        """ Adds move preview event to the event list """

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
