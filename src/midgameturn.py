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
