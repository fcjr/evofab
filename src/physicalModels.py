from printer import Printer
from camera import Camera
from evocontroller.evoPyLib.evoPyLib import *
from evocontroller.evoCamera.evoCamera import EvoCamera
import time

class PhysicalPrinter(Printer):
    def __init__(self,port,time_interval):
        self.port = port
        self.time_interval = time_interval
        self.e = EvoController(port)
        self.STOP = "+000+000"
        self.velocity = "+000+000"

    def setPenUp(self):
        self.e.pause()

    def setPenDown(self):
        self.e.extrude()

    def simulate(self):
        self.e.changeVelocity(self.velocity)
        time.sleep(time_interval)
        self.e.changeVelocity(self.STOP)

    def set_printer_direction(self, leftright, updown):
        """Set the direction the printer will move in on the following time steps.

        leftright: -1 = left motion, 0 = no leftright motion, 1 = right motion
        updown: -1 = down motion, 0 = no updown motion, 1 = up motion"""

        x = "+000"
        y = "+000"

        if leftright == -1:
            x = "-025"
        elif leftright == 1:
            x = "+025"

        if updown == -1:
            y = "-025"
        elif updown == 1:
            y = "+025"


        self.velocity = x+y

    def set_position_on_grid(self, xcell, ycell):
        """ Move the printer to the specified cell position on the grid"""
        pass


    def move_is_valid(self):
        """ Checks if moving with the given dt will cause collision with the boundaries of the grid """
        return True


class PhysicalCamera(Camera):
        def __init__(port):
            self.port = port
            self.e = EvoCamera(port)

        def all_cell_values(self):
            output = self.e.getVals()
            return output

        def gridsize(self):
            return 0

        def num_cells_in_view(self, gridcell):
            return 0

        def get_4_cell_topleft_factor(self, topleft_cell_corner):
            return 0

        def get_4_cell_topright_factor(self, topright_cell_corner):
            return 0

        def get_4_cell_bottomleft_factor(self, bottomleft_cell_corner):
            return 0

        def get_4_cell_bottomright_factor(self, bottomright_cell_corner):
            return 0
