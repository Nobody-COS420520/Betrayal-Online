"""Main Module for Betrayal at the House on the Hill by Nobody"""

#import sys
#sys.path.append('./src/')
#import pgzrun
#import pygzero_funcs
#import midgame
#import example


WIDTH = 960
HEIGHT = 540
TITLE = "Betrayal Online"


#def main():
#    """The Main Function"""

#    print("hello world!")
#    print(example.example_func(100))
#
#    _game_state = 0
#
#    print("Entering _game_state switch")
#    _game_state = 2
#    match _game_state:
#        case 2:     #   case: Midgame

#            print("beginning of switch")
#            midgame.setup_midgame(WIDTH, HEIGHT)
#            print("before draw")
#            midgame.draw()
  
def draw():
    """ need this"""

    screen.clear()

    _game_state = 0

    print("Entering _game_state switch")
    _game_state = 2
    match _game_state:
        case 2:     #   case: Midgame
            print("beginning of switch")
            setup_midgame(WIDTH, HEIGHT) #TODO
            print("before draw")
            draw() #TODO
            #screen.blit("bo_specific/dark_wood_texture.jpg", (0,0))
            
            #bg = Actor("bo_specific/dark_wood_texture.jpg", topleft=(0,0))
            #bg.draw()


pgzrun.go()