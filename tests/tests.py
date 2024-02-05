"""Module to hold all of our tests"""
import sys
sys.path.append('..')
sys.path.append('../src')
from src import example   #pylint: disable=wrong-import-position



def test_example_func():
    """Test for example_func from src/example.py"""
    assert example.example_func(4) == '4 OK!!'
