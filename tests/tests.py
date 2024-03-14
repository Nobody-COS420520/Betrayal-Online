"""Module to hold all of our tests"""
#pylint: disable=wrong-import-position
import sys
sys.path.append('..')
sys.path.append('../src')
from src import example
from src import midgame

GRID_SIZE = 150
GRID_OFFSET_X = 50


def test_example_func():
    """ Test for example_func() from src/example.py"""
    assert example.example_func(4) == '4 OK!!'

def test_src_initialize_grid():
    """ Test for initialize_grid() from src/midgame.py"""
    test_assert = []
    test_width = 480
    test_height = 270

    for x in range(0, test_width//midgame.GRID_SIZE):
        test_assert.append([])
        for y in range(0, test_height//midgame.GRID_SIZE):
            test_assert[x].append(midgame.GridSquare(x,y))

    assert midgame.initialize_grid(480, 270) == test_assert

def test_src_GridSquare_get_x():
    """ Test for GridSquare.get_x() from src/midgame.py"""
    test_square = midgame.GridSquare(5,6)

    assert test_square.get_x() == 800
