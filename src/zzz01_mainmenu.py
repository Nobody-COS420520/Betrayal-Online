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
        self.actors.append(Actor("bo_specific/main-menu-bg-1920x1080.png"))
        self.actors.append(Actor("bo_specific/betrayal_logo_transparent_1920x1080.png",
                           midtop=(WIDTH/2-WIDTH/48, HEIGHT/10-HEIGHT/21)))
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
            x.text.fontsize = 64
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
        p_menu_object.text.fontsize = 82

    @staticmethod
    def on_offhover(p_menu_object):
        """ Executes on offhover over MainMenu menu object """
        p_menu_object.text.fontsize = 64
        p_menu_object.highlight_flag = 0

    @staticmethod
    def on_mouseup(p_menu_object):
        """ Executes on hover over MainMenu menu object """
        p_menu_object.highlight_flag = 1

    @staticmethod
    def online_mouseup(p_menu_object):
        """ Goes into GAME_STAGE 2 (Midgame) when 'ONLINE' gets pressed """
        # TODO change this when midgame gets modernized
        global GAME_STAGE
        GAME_STAGE = 2
