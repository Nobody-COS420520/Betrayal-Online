""" Holds class definition for menu objects which contain menu object"""
# pylint: disable=C0301, C0305, R0902


class Menu_Tree():
    """ Holds Tree graph holding Menu_Object instances and their relation """

    contents = []

    def __init__(self):
        """ Menu_Tree Constructor """
        self.contents = []
        pass

    def add(self, text, rect=Rect((25, 25), (100, 100))):
        """ Appends a new Menu_Object into the Menu_Tree """
        self.contents.append(self.Menu_Object(text, rect))

    def draw(self):
        """ Draws all Menu Objects in Menu_Tree. Used in main draw() function """
        for x in self.contents:
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
