import pygame
from settings import *

state_images_cords = [(8, 39, 18, 18), (8, 71, 18, 18), (8, 103, 18, 18),
                (141, 104, 18, 18), (141, 72, 18, 18), (141, 40, 18, 18)]

move_images_cords = [(41, 7, 22, 18), (38, 40, 25, 18), (39, 72, 23, 18), (38, 104, 22, 18)]

def cords(c):
    return c[0], c[1], c[2], c[3]


class Person:
    def __init__(self, x, y, name):
        print('person')
        self.x = x
        self.y = y
        self.name = name
        self.pos = (self.x // TILE, self.y // TILE)
        self.want_move = self.pos

        self.state_images = [pygame.image.load(f'templates/persons/{name}.png').subsurface(cords(i))
                             for i in state_images_cords]
        for i in range(len(self.state_images)):
            self.state_images[i] = pygame.transform.scale(self.state_images[i], (100, 100))

        self.move_images = [pygame.image.load(f'templates/persons/{name}.png').subsurface(cords(i))
                            for i in move_images_cords]
        for i in range(len(self.move_images)):
            self.move_images[i] = pygame.transform.scale(self.move_images[i], (100, 100))

        self.img = None

    def get_big_pos(self):
        return (self.pos[0] * TILE, self.pos[1] * TILE)

    def move(self, cords):
        if self.pos != self.want_move:
            cords.reverse()
            cord = cords[0]
            if self.y < cord[1] * TILE:
                self.y += 4
            elif self.y > cord[1] * TILE:
                self.y -= 4
            elif self.x < cord[0] * TILE:
                self.x += 4
            elif self.x > cord[0] * TILE:
                self.x -= 4
            else:
                self.pos = cord
                cords.reverse()
                cords.remove(cord)
                cords.reverse()
            cords.reverse()
        return cords

    def choice_image(self):
        pass

