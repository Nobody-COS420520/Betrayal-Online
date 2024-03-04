"""Module to hold all of our tests"""
import sys
sys.path.append('..')
sys.path.append('../src')
from src import example   #pylint: disable=wrong-import-position
from src import midgame


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
