import unittest
from vector import Vector
from camera import Camera
from grid import Grid
from gridworld import GridWorld
from virtualprinter import VirtualPrinter
import pygame

class TestCamera(unittest.TestCase):
    def setUp(self):
        self.gridworld = GridWorld(20, 20, 10) 
        self.printer = VirtualPrinter(0, 0, 10, 1, pygame.color.Color("darkorange"), self.gridworld)
        self.grid = self.gridworld.grid
        self.camera = Camera(self.grid, self.printer, 3)

    def test_camera_has_correct_values_at_init(self):
        self.assertIs(self.camera.world_grid, self.gridworld.grid)
        self.assertIs(self.camera.printer, self.printer)
        self.assertEqual(self.camera.n, 3)
        self.assertEqual(self.camera.cell_width, self.gridworld.gridsize())

    def test_num_cells_in_view_isnt_wrong(self):
        #one cell
        self.printer.position = Vector(15, 15)
        self.assertEqual(self.camera.num_cells_in_view(Vector(1, 1)), 1)
        #two cell
        self.printer.position = Vector(15, 12)
        self.assertEqual(self.camera.num_cells_in_view(Vector(1, 1)), 2)
        #red cell
        self.printer.position = Vector(12, 12)
        self.assertEqual(self.camera.num_cells_in_view(Vector(1, 1)), 4)
        #blue cell

    def test_cells_in_view_independent_of_camera_size(self):
        local_camera = Camera(self.grid, self.printer, 4)
        self.printer.position = Vector(30, 30)
        self.assertEqual(local_camera.num_cells_in_view(Vector(1, 1)), 1)
        #two cell
        self.printer.position = Vector(30, 32)
        self.assertEqual(local_camera.num_cells_in_view(Vector(1, 1)), 2)
        #red cell
        self.printer.position = Vector(32, 32)
        self.assertEqual(local_camera.num_cells_in_view(Vector(1, 1)), 4)

    def test_cells_have_same_result_for_cells_in_view(self):
        #one cell
        self.printer.position = Vector(15, 15)
        self.assertEqual(self.camera.num_cells_in_view(Vector(3, 3)), 1)
        #two cell
        self.printer.position = Vector(15, 12)
        self.assertEqual(self.camera.num_cells_in_view(Vector(3, 3)), 2)
        #red cell
        self.printer.position = Vector(12, 12)
        self.assertEqual(self.camera.num_cells_in_view(Vector(3, 3)), 4)
        #blue cell
    
    def test_region_aligned(self):
        self.printer.position = Vector(15, 15)
        self.grid.set_loc_val(1, 1, 3)
        self.assertEqual(self.camera.percent_in_view(Vector(1, 1)), 3)

    def test_region_over_two_cells_horizontally_aligned(self):
        self.printer.position = Vector(15, 20)
        self.grid.set_loc_val(1, 1, 1)
        self.grid.set_loc_val(1, 2, 0)
        self.assertEqual(self.camera.percent_in_view(Vector(1, 1)), 0.5)

    def test_region_over_two_cells_vertically_aligned(self):
        self.printer.position = Vector(20, 15)
        self.grid.set_loc_val(1, 1, 1)
        self.grid.set_loc_val(2, 1, 0)
        self.assertEqual(self.camera.percent_in_view(Vector(1, 1)), 0.5)
        self.printer.position = Vector(22, 15)
        self.grid.set_loc_val(1, 1, 1)
        self.grid.set_loc_val(2, 1, 0)
        self.assertEqual(self.camera.percent_in_view(Vector(1, 1)), 0.7)

    def test_region_over_four_cells(self):
        self.printer.position = Vector(20, 20)
        self.grid.set_loc_val(1, 1, 1)
        self.grid.set_loc_val(2, 1, 0)
        self.grid.set_loc_val(1, 2, 0)
        self.grid.set_loc_val(2, 2, 0)
        self.assertEqual(self.camera.percent_in_view(Vector(1, 1)), 0.25)

    def test_region_over_four_cells_with_arbitrary_camera_size(self):
        localcamera = Camera(self.grid, self.printer, 5)
        self.printer.position = Vector(20, 20)
        self.grid.set_loc_val(1, 1, 1)
        self.grid.set_loc_val(2, 1, 0)
        self.grid.set_loc_val(1, 2, 0)
        self.grid.set_loc_val(2, 2, 0)
        self.assertEqual(self.camera.percent_in_view(Vector(1, 1)), 0.25)
