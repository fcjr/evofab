from pygame import *
import colorsys
from evocontroller.evoPyLib.evoPyLib import *
import argparse


class Visualizer:

    """Constructs a Visualizer that uses the given initial_photo values (iterable
    of length 8 iterables with photo resistor values) and given buffer_value to
    set the intensity ranges for the visual display"""
    def __init__(self, initial_photo, buffer_value = 5, dimensions = (600, 400)):
        self.buffer_value = buffer_value
        self.min_val = min([min(x) for x in initial_photo]) - buffer_value
        self.max_val = max([max(x) for x in initial_photo]) + buffer_value
        self.screen = display.set_mode(dimensions)
        background_colour = (255,255,255)
        screen = self.screen
        screen.fill(background_colour)
        self.rects = []
        self.rects.append(Rect((20, 20), (40, 40)))
        self.rects.append(Rect((80, 20), (40, 40)))
        self.rects.append(Rect((140, 20), (40, 40)))
        self.rects.append(Rect((140, 80), (40, 40)))
        self.rects.append(Rect((140, 140), (40, 40)))
        self.rects.append(Rect((80, 140), (40, 40)))
        self.rects.append(Rect((20, 140), (40, 40)))
        self.rects.append(Rect((20, 80), (40, 40)))

        self.inputs = []
        for i in range(8):
            self.inputs.append(Rect((300 + (i * 30), 20), (20, 20)))
        display.flip()

    def get_val(self, photo_val):
        intensity = (photo_val - self.min_val)/float(self.max_val - self.min_val)
        return 1 - intensity

    def update(self, photo_values, output='+000+030'):
        for n,v in enumerate(photo_values):
            if v < self.min_val:
                self.min_val = v
            elif v > self.max_val:
                self.max_val = v
            inten = self.get_val(v)
            color = map(lambda x: 100 * x, colorsys.hsv_to_rgb(.5, 0, inten))
            self.screen.fill(color, self.rects[n])
            self.screen.fill(color, self.inputs[n])
            #draw each of the directional arrows
            x_vel = output[:4]
            y_vel = output[4:]
            c = (Color('red'), Color('green'))
            up = down = left = right = 0
            if x_vel[2] == '0':
                left = 0
                right = 0
            elif x_vel[0] == '+':
                right = 1
            else:
                left = 1
            if y_vel[2] == '0':
                down = 0
                up = 0
            elif y_vel[0] == '+':
                down = 1
            else:
                up = 1
            draw.polygon(self.screen, c[up], ((420, 80), (440, 120), (400, 120)))
            draw.polygon(self.screen, c[down], ((420, 180), (440, 140), (400, 140)))
            draw.polygon(self.screen, c[left], ((360, 130), (400, 110), (400, 150)))
            draw.polygon(self.screen, c[right], ((480, 130), (440, 110), (440, 150)))
        display.flip()

if __name__ == "__main__":
    ap = argparse.ArgumentParser()

    ap.add_argument("-p", "--port", help = "sensor array port")
    args = vars(ap.parse_args())

    port = args["port"]
    sense = EvoArray(port)

    visualizer = Visualizer([sense.getNext() for x in range(10)])
    init_photo_vals = sense.getNext()
    while True:
        vals = sense.getNext()
        vals = [(x - y) * (x - y) for x,y in zip(vals, init_photo_vals)]
        print vals
        visualizer.update(vals)
