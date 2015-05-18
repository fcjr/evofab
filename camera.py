from grid import Grid
from virtualprinter import VirtualPrinter
import pygame

def x(collection):
    return collection[0]

def y(collection):
    return collection[1]

def same_x(pair1, pair2):
    return x(pair1) == x(pair2)

def same_y(pair1, pair2):
    return y(pair1) == y(pair2)

class Camera:

    def __init__(self, printer, grid, size=3):
        self.printer = printer
        self.grid = grid
        self.width = grid.width
        self.scale = grid.gridsize
        self.size = size

    def get_ratio_filled_in_view(self, grid_cell):
        """ gets the percentage filled of the space in view of the given
        grid cell"""

        in_view = self.get_cells_in_view(grid_cell)
        in_view = [(int(a), int(b)) for a, b in in_view]
        pixel_cell = self.get_pixel_coords(grid_cell)
        if len(in_view) == 4:
            q0_weight = self.get_weight_factor_for_one_of_four(in_view[0])
            q1_weight = self.get_weight_factor_for_one_of_four(in_view[1])
            q2_weight = self.get_weight_factor_for_one_of_four(in_view[2])
            q3_weight = self.get_weight_factor_for_one_of_four(in_view[3])
            percentage = (
                    q0_weight * self.grid.val_at(x(in_view[0]), y(in_view[0])) +
                    q1_weight * self.grid.val_at(x(in_view[1]), y(in_view[1])) +
                    q2_weight * self.grid.val_at(x(in_view[2]), y(in_view[2])) +
                    q3_weight * self.grid.val_at(x(in_view[3]), y(in_view[3]))
                    )
            return percentage
        elif len(in_view) == 2:
            if same_x(in_view[0], in_view[1]):
                factor1 = (self.width - (y(self.get_pixel_coords(in_view[0])) % self.width)) / self.width
                factor2 = (self.width - (y(self.get_pixel_coords(in_view[1])) % self.width)) / self.width
            else:
                factor1 = (self.width - (x(self.get_pixel_coords(in_view[0])) % self.width)) / self.width
                factor2 = (self.width - (x(self.get_pixel_coords(in_view[1])) % self.width)) / self.width
            percentage = factor1 * self.grid.val_at(x(in_view[0]), y(in_view[0])) + factor2 * self.grid.val_at(x(in_view[1]), y(in_view[1]))
            return percentage
        elif len(in_view) == 1:
            return self.grid.val_at(x(in_view[0]), y(in_view[0]))
        else:
            assert True == False #explode if there's an unreasonable number of cells in view

    def get_weight_factor_for_one_of_four(self, cell_in_view):
        quada = (self.width - (x(self.get_pixel_coords(cell_in_view))) % self.width)
        quadb = (self.width - (y(self.get_pixel_coords(cell_in_view))) % self.width)
        weight = (quada * quadb) / (self.width * self.width) #weight based on the area of cell in view/area of the cell
        return weight
    
    def get_cells_in_view(self, camera_cell):
        """ will return a list of tuples containing the x,y grid coordinates of
        the cells which are overlapped by the given camera cell """

        in_view = []

        cam_cell_x, cam_cell_y = self.get_pixel_coords(camera_cell)

        top_left_diff = (cam_cell_x % self.width, cam_cell_y % self.width)

        top_left = (cam_cell_x - x(top_left_diff), cam_cell_y - y(top_left_diff))
        in_view.append(self.get_cell_coords(top_left))
        if (x(top_left_diff) != 0): #if the x coordinates don't line up
            if (y(top_left_diff) != 0): #if the y coordinates don't line up
                in_view.append(self.get_cell_coords((x(top_left), y(top_left) + self.width)))
                in_view.append(self.get_cell_coords((x(top_left) + self.width, y(top_left))))
                in_view.append(self.get_cell_coords((x(top_left) + self.width, y(top_left) + self.width)))
            else:
                in_view.append(self.get_cell_coords((x(top_left) + self.width, y(top_left))))
        elif (y(top_left_diff) != 0):
                in_view.append(self.get_cell_coords((x(top_left), y(top_left) + self.width)))

        #ignore cells that would be off the build platform
        in_view = [(a, b) for a,b in in_view if (a >= 0 and b >= 0) and (a < self.size * self.width and b < self.size * self.width)]
        return in_view

    def get_pixel_coords(self, cell_coord):
        upper_center_corner = (self.printer.position.x - self.width/2.0, self.printer.position.y - self.width/2.0)
        assert isinstance(self.size, int) == True #to keep the next line from not doing what it's supposed to do
        upper_camera_corner = self.get_upper_corner()
        pixel_coords = (x(upper_camera_corner) + (x(cell_coord) * self.width), y(upper_camera_corner) + (y(cell_coord) * self.width))
        return pixel_coords

    def get_upper_corner(self):
        #upper_camera_corner = (x(upper_center_corner) - self.size/2, y(upper_center_corner) - self.size/2) #line below fixes this broken line
        upper_center_corner = (self.printer.position.x - self.width/2.0, self.printer.position.y - self.width/2.0)
        return (x(upper_center_corner) - self.width, y(upper_center_corner) - self.width) #TODO this assumes that camera is size 3

    def get_cell_coords(self, pixel_coord):
        return (x(pixel_coord)/self.width, y(pixel_coord)/self.width)

    def draw(self, window):
        corner = self.get_upper_corner()
        for i in xrange(0, self.size):
            pygame.draw.line(
                    window,
                    pygame.color.Color("black"),
                    (x(corner), y(corner) + (self.scale * i)),
                    (x(corner) + (self.scale * self.size), y(corner) + (self.scale * i))
                    )
            pygame.draw.line(
                    window,
                    pygame.color.Color("black"),
                    (x(corner) + (self.scale * i), y(corner)),
                    (x(corner) + (self.scale * i), y(corner) + (self.scale * self.size))
                    )
