from grid import Grid
import unittest

class GridTests(unittest.TestCase):
    def setUp(self):
        self.grid = Grid(10, 10, 5)

    def test_init_from_file(self):
        grid = Grid(scale=7, path='test/resources/example')
        self.assertEqual(grid.grid, [ [0,1,0,1,0,1,0,1,0,1], [1,0,1,0,1,0,1,0,1,0], [1,1,1,1,1,1,1,1,1,1], [0,1,0,1,0,1,0,1,0,1] ])

    def test_value_changes(self):
        self.grid.set_loc_val(3, 3, 1)
        assert self.grid.val_at(3, 3) == 1

        self.grid.set_loc_val(1, 5, 3)
        assert self.grid.val_at(1, 5) == 3
