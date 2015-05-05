from grid import Grid
from virtualprinter import VirtualPrinter

class Camera:

    def __init__(self, printer, grid, size=3):
        self.printer = printer
        self.grid = grid
        self.width = grid.width
        self.size = size

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
        #upper_camera_corner = (x(upper_center_corner) - self.size/2, y(upper_center_corner) - self.size/2) #line below fixes this broken line
        upper_camera_corner = (x(upper_center_corner) - self.width, y(upper_center_corner) - self.width) #TODO this assumes that camera is size 3
        pixel_coords = (x(upper_camera_corner) + (x(cell_coord) * self.width), y(upper_camera_corner) + (y(cell_coord) * self.width))
        return pixel_coords

    def get_cell_coords(self, pixel_coord):
        return (x(pixel_coord)/self.width, y(pixel_coord)/self.width)

def x(collection):
    return collection[0]

def y(collection):
    return collection[1]
