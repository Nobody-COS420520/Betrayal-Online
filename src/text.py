""" Holds Text class which holds all instance data needed for pygame zero text """


class Text():
    """ Holds all instance data needed for pygame zero text """
    text = ""  # Holds the text of a Menu_object
    fontname = "Calibri"  # Holds fontname of Menu_object's text
    fontsize = 24  # Holds fontsize of Menu_object's text
    antialias = True  # Flag for text to be rendered with antialias, default is True
    color = "white"  # Holds color of text
    background = None  # Holds background color for text to use

    top = None  # Positional variables
    left = None
    bottom = None
    right = None
    topleft = None
    bottomleft = None
    topright = None
    bottomright = None
    midtop = None
    midleft = None
    midbottom = None
    midright = None
    center = None
    centerx = None
    centery = None

    width = None  # Holds width of text for formatting
    widthem = None  # Holds width of text in em
    lineheight = 1.0  # Holds vertical spacing between lines in units of font's default height
    #   Can prevent line wrapping by including non-breaking space chars: \u00A0

    align = None  # Holds horizontal positioning of text

    owidth = None  # Holds outline width in outline units
    ocolor = "black"  # Holds outline color

    # Holds (x,y) values representing the drop shadow offset in shadow units
    shadow = None
    scolor = "black"  # Holds drop shadow color

    gcolor = None  # Holds lower gradient stop color

    alpha = 1.0  # Holds alpha transparency, range from 0.0-1.0

    anchor = (0.0, 0.0)  # Holds anchor position, range from 0.0-1.0

    angle = 0  # Holds counterclockwise rotational value in deg
    #   Pygame Zero rounds to nearest multiple of 3 deg

    highlight_color = "black"

    def __init__(self, text, fontname="Calibri", fontsize=24, antialias=True,
                 color="white", background=None, top=None, left=None,
                 bottom=None, right=None, topleft=None, bottomleft=None,
                 topright=None, bottomright=None, midtop=None, midleft=None,
                 midbottom=None, midright=None, center=None, centerx=None,
                 centery=None, width=None, widthem=None, lineheight=1.0,
                 align=None, owidth=None, ocolor="black", shadow=None,
                 scolor="black", gcolor=None, alpha=1.0, anchor=(0.0, 0.0),
                 angle=0, highlight_color="black"):
        self.text = text
        self.fontname = fontname
        self.fontsize = fontsize
        self.antialias = antialias
        self.color = color
        self.background = background
        self.top = top
        self.left = left
        self.bottom = bottom
        self.right = right
        self.topleft = topleft
        self.bottomleft = bottomleft
        self.topright = topright
        self.bottomright = bottomright
        self.midtop = midtop
        self.midleft = midleft
        self.midbottom = midbottom
        self.midright = midright
        self.center = center
        self.centerx = centerx
        self.centery = centery
        self.width = width
        self.widthem = widthem
        self.lineheight = lineheight
        self.align = align
        self.owidth = owidth
        self.ocolor = ocolor
        self.shadow = shadow
        self.scolor = scolor
        self.gcolor = gcolor
        self.alpha = alpha
        self.anchor = anchor
        self.angle = angle
        self.highlight_color = highlight_color

    def draw(self):
        """ Draws a text item. Used in main draw() function """
        screen.draw.text(self.text, fontname=self.fontname, fontsize=self.fontsize,
                         antialias=self.antialias, color=self.color,
                         background=self.background, top=self.top, left=self.left,
                         bottom=self.bottom, right=self.right, topleft=self.topleft,
                         bottomleft=self.bottomleft, topright=self.topright,
                         bottomright=self.bottomright, midtop=self.midtop, midleft=self.midleft,
                         midbottom=self.midbottom, midright=self.midright, center=self.center,
                         centerx=self.centerx, centery=self.centery, width=self.width,
                         widthem=self.widthem, lineheight=self.lineheight, align=self.align,
                         owidth=self.owidth, ocolor=self.ocolor, shadow=self.shadow, scolor=self.scolor,
                         gcolor=self.gcolor, alpha=self.alpha, anchor=self.anchor, angle=self.angle)
