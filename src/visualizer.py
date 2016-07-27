import pygame
import colorsys

class Visualizer:

    """Constructs a Visualizer that uses the given initial_photo values (iterable
    of length 8 iterables with photo resistor values) and given buffer_value to
    set the intensity ranges for the visual display"""
    def __init__(self, initial_photo, buffer_value = 50, dimensions = (600, 400)):
        self.buffer_value = 50
        self.min_val = min([min(x) for x in initial_photo)]) - buffer_value
        self.max_val = max([max(x) for x in initial_photo)]) + buffer_value
        self.screen = pygame.display.set_mode(dimensions)
        background_colour = (255,255,255)
        screen.fill(background_colour)
        self.rects = []
        self.rects[1] = pygame.draw.rect(screen, (0, 0, 0), (20, 20, 40, 40), 2)
        self.rects[2] = pygame.draw.rect(screen, (0, 0, 0), (80, 20, 40, 40), 2)
        self.rects[3] = pygame.draw.rect(screen, (0, 0, 0), (140, 20, 40, 40), 2)
        self.rects[4] = pygame.draw.rect(screen, (0, 0, 0), (140, 80, 40, 40), 2)
        self.rects[5] = pygame.draw.rect(screen, (0, 0, 0), (140, 140, 40, 40), 2)
        self.rects[6] = pygame.draw.rect(screen, (0, 0, 0), (20, 140, 40, 40), 2)
        self.rects[7] = pygame.draw.rect(screen, (0, 0, 0), (80, 140, 40, 40), 2)
        self.rects[8] = pygame.draw.rect(screen, (0, 0, 0), (20, 80, 40, 40), 2)
        pygame.display.flip()

    def get_val(self, photo_val):
        intensity = photo_val * 100/float(self.max_val - self.min_val)
        return intensity

    def update(self, photo_values):
        for n,v in enumerate(photo_values):
            inten = self.get_val(v)
            color = colorsys.hsv_to_rgb(187, 0, intensity)
            self.rects[n].fill(color)
        pygame.display.flip()
