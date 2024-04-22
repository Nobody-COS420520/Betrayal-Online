"""Example Module to Test Things"""
import numpy

def example_func(p_num):
    """Test Function, Returns a String"""
    return str(p_num) + " OK!!!"


def test_example_func():
    """Unit Test for example_func"""
    assert example_func(4) == "4 OK!!"
