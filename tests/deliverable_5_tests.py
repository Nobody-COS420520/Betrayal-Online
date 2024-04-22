import unittest
import math

class MockMidgame:
    def __init__(self):
        self.grid = []
        self.grid_size = 50

    def initialize_grid(self, width, height):
        grid_width = math.ceil(width / self.grid_size)
        grid_height = math.ceil(height / self.grid_size)
        self.grid = [[MockCell((i, j)) for j in range(grid_height)] for i in range(grid_width)]

    def cam_move_hori(self, delta_px):
        for row in self.grid:
            for cell in row:
                cell.rect.topleft = (cell.rect.topleft[0] + delta_px, cell.rect.topleft[1])

class MockCell:
    def __init__(self, position):
        self.rect = MockRect(position)

class MockRect:
    def __init__(self, topleft):
        self.topleft = topleft

class TestMidgame(unittest.TestCase):
    def setUp(self):
        self.midgame = MockMidgame()

    def test_initialize_grid_valid(self):
        width = 800
        height = 600
        self.midgame.initialize_grid(width, height)

        grid_width = len(self.midgame.grid)
        grid_height = len(self.midgame.grid[0])
        expected_width = math.ceil(width / self.midgame.grid_size)
        expected_height = math.ceil(height / self.midgame.grid_size)
        self.assertEqual(grid_width, expected_width)
        self.assertEqual(grid_height, expected_height)

        width = -2
        height = 500
        self.midgame.initialize_grid(width, height)

        grid_width = len(self.midgame.grid)
        grid_height = -1 if grid_width == 0 else len(self.midgame.grid[0])
        expected_width = math.ceil(width / self.midgame.grid_size)
        expected_height = math.ceil(height / self.midgame.grid_size)
        self.assertEqual(grid_width, expected_width)
        self.assertNotEqual(grid_height, expected_height)



    def test_cam_move_hori(self):
        width = 800
        height = 600
        self.midgame.initialize_grid(width, height)

        initial_positions = []
        for row in self.midgame.grid:
            for cell in row:
                initial_positions.append(cell.rect.topleft)

        delta_px = 100
        self.midgame.cam_move_hori(delta_px)

        for i, row in enumerate(self.midgame.grid):
            for j, cell in enumerate(row):
                expected_x = initial_positions[i * len(row) + j][0] + delta_px
                expected_y = initial_positions[i * len(row) + j][1]
                self.assertEqual(cell.rect.topleft, (expected_x, expected_y))

                
def return_true():
    return True

class TestCase(unittest.TestCase):
    def test_test(self):
        self.assertTrue(return_true())



# This line runs all tests in classes inheriting from unittest.TestCase
if __name__ == '__main__':
    unittest.main()

