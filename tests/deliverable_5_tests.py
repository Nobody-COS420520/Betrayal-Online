""" Module containing tests to be graded for Deliverable 5 """

import unittest

def return_true():
    return True

class test_case(unittest.TestCase):

    def test_test(self):
        self.assertTrue(return_true())


# This line runs all tests in classes inheriting from unittest.TestCase
if __name__ == '__main__':
    unittest.main()

