import pygame
from settings import *

images_cords = [(8, 39, 18, 18), (8, 71, 18, 18), (8, 103, 18, 18),
                (141, 104, 18, 18), (141, 72, 18, 18), (141, 40, 18, 18)]


def cords(c):
    return c[0], c[1], c[2], c[3]


class Person:
    def __init__(self, x, y, name):
        self.pos = (x, y)
        self.state_images = [pygame.image.load(f'templates/persons/{name}.png').subsurface(cords(i)) for i in images_cords]
        for i in range(len(self.state_images)):
            self.state_images[i] = pygame.transform.scale(self.state_images[i], (100, 100))

    def get_big_pos(self):
        return (self.pos[0] * TILE, self.pos[1] * TILE)

    def move(self, pos):
        self.pos = pos

