import pygame
from settings import *


class Person:
    def __init__(self, x, y, name):
        self.pos = (x, y)
        self.name = name
        self.images = {
            'state': pygame.transform.scale(pygame.image.load('templates/persons/eliwood(lord)/state.png'), (80, 80))
        }

    def get_big_pos(self):
        return (self.pos[0] * TILE, self.pos[1] * TILE)

    def move(self, pos):
        self.pos = pos

