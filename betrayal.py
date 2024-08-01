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
