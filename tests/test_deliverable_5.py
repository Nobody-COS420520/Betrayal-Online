import unittest

class mockMidgame():
    def zoom(self, grid_size_modifier):
        """ Updates global GRID_SCALE var and scales+moves Rect objs in GRID
            grid_size_modifer = percent (decimal form) modifier global GRID vars are multiplied against """

        self.grid_size *= grid_size_modifier
        self.grid_scale *= grid_size_modifier
        self.grid_offset_x *= grid_size_modifier
        self.grid_offset_y *= grid_size_modifier

        #   reset highlight flags for GRID squares to prevent lingering remnants
        # for x in range(len(GRID)):
        #    for y in range(len(GRID[0])):
        #        GRID[x][y].highlight_flag = 0

        # pylint: disable-next=C0200
        for x in range(len(self.grid)):

            for y in range(len(self.grid[x])):
                # x_pos = GRID[x][y].hori*GRID_SIZE+GRID_OFFSET_X
                # y_pos = GRID[x][y].vert*GRID_SIZE+GRID_OFFSET_Y
                x_pos = self.grid[x][y].get_x()
                y_pos = self.grid[x][y].get_y()
                self.grid[x][y].rect = Rect(
                    x_pos, y_pos, self.grid_size, self.grid_size)
                if (self.grid[x][y].actor is not None):
                    self.establish_actor(self.grid[x][y])
                    self.grid[x][y].floortile.update_enclosed_actors()

        return self.grid_scale
    
class mockFloorGrid():
    def setup_floor_neighbors(self, p_floorgridlist):
        #    p_floorgridlist expected index format:
        #    0 = Basement, 1 = Ground, 2 = Upper

        self.neighbors = [None]*2
        if (self.floorid == "Basement"):
            self.neighbors[1] = p_floorgridlist[1]
            self.contents[0].neighbors.add(
                p_floorgridlist[1].contents[3], "Special", 5)
            self.contents[0].doors.append(False)
            self.contents[0].doors.append(True)
        elif (self.floorid == "Ground"):
            self.neighbors[0] = p_floorgridlist[0]
            self.neighbors[1] = p_floorgridlist[2]
            for x in range(4):
                if x-1 >= 0:
                    self.contents[x].neighbors.add(self.contents[x-1], "Right")
                if x+1 < 4:
                    self.contents[x].neighbors.add(self.contents[x+1], "Left")
                if x == 3:
                    self.contents[x].neighbors.add(
                        p_floorgridlist[0].contents[0], "Special", 4)
                    self.contents[x].neighbors.add(
                        p_floorgridlist[2].contents[0], "Special", 5)
                    self.contents[x].doors.append(True)
                    self.contents[x].doors.append(True)
        elif (self.floorid == "Upper"):
            self.neighbors[0] = p_floorgridlist[1]
            self.contents[0].neighbors.add(
                p_floorgridlist[1].contents[3], "Special", 4)
            self.contents[0].doors.append(True)

def test_grid_setup_and_zoom_valid(self):
    # Define valid grid dimensions and grid size
    p_width = 100
    p_height = 100
    grid_size = 10

    # Set up the grid in your instance
    self.midgame.setup_grid(p_width, p_height, grid_size)

    # Define valid grid size modifier for zooming
    grid_size_modifier = 1.5

    # Call the method to establish grid neighbors
    self.midgame.establish_grid_neighbors(p_width, p_height)

    # Call the zoom method with valid parameters
    self.midgame.zoom(grid_size_modifier)

    # Assert that grid size and scale are updated correctly after zooming
    self.assertEqual(self.midgame.grid_size, grid_size * grid_size_modifier)
    self.assertEqual(self.midgame.grid_scale, grid_size * grid_size_modifier)

    # Iterate through each grid square and test its neighbors and rectangle
    for x in range(p_width // grid_size):
        for y in range(p_height // grid_size):
            # Get the current grid square
            grid_square = self.midgame.grid[x][y]

            # Test Up neighbor
            if y != 0:
                self.assertEqual(grid_square.neighbors[0], self.midgame.grid[x][y - 1])
            else:
                self.assertIsNone(grid_square.neighbors[0])

            # Test Left neighbor
            if x != 0:
                self.assertEqual(grid_square.neighbors[1], self.midgame.grid[x - 1][y])
            else:
                self.assertIsNone(grid_square.neighbors[1])

            # Test Right neighbor
            if x != p_width // grid_size - 1:
                self.assertEqual(grid_square.neighbors[2], self.midgame.grid[x + 1][y])
            else:
                self.assertIsNone(grid_square.neighbors[2])

            # Test Down neighbor
            if y != p_height // grid_size - 1:
                self.assertEqual(grid_square.neighbors[3], self.midgame.grid[x][y + 1])
            else:
                self.assertIsNone(grid_square.neighbors[3])

            # Test that the rectangle dimensions are updated correctly after zooming
            self.assertEqual(grid_square.rect.width, grid_size * grid_size_modifier)
            self.assertEqual(grid_square.rect.height, grid_size * grid_size_modifier)

            # Test that the rectangle position is updated correctly after zooming
            expected_x_pos = grid_square.get_x() * grid_size_modifier
            expected_y_pos = grid_square.get_y() * grid_size_modifier
            self.assertEqual(grid_square.rect.x, expected_x_pos)
            self.assertEqual(grid_square.rect.y, expected_y_pos)

def test_zoom_invalid_parameters(self):
    # Define invalid grid size modifier for zooming
    invalid_grid_size_modifier = -1

    # Call the zoom method with invalid parameters
    with self.assertRaises(ValueError):
        self.midgame.zoom(invalid_grid_size_modifier)


if __name__ == '__main__':
    unittest.main()