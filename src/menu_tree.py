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
