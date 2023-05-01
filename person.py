import pygame
from settings import *

state_images_cords = [(1, 33, 31, 31), (1, 65, 31, 31), (1, 97, 31, 31),
                      (133, 97, 31, 31), (133, 65, 31, 31), (133, 33, 31, 31)]

move_images_cords = [(34, 65, 31, 31), (34, 97, 31, 31),
                     (67, 1, 31, 31), (67, 65, 31, 31),
                     (100, 1, 31, 31), (100, 65, 31, 31)]


def cords(c):
    return c[0], c[1], c[2], c[3]


class Person:
    def __init__(self, x, y, name, color='B'):
        print('person')
        self.x = x
        self.y = y
        self.name = name
        self.state = 'stay'
        self.pos = (self.x // TILE, self.y // TILE)
        self.want_move = self.pos
        self.move_to = ''

        self.hp = 100
        self.damage = 20
        self.armor = 20
        self.critical = 100

        self.can_fight_with = []
        self.attack_button = None

        self.stay_images = [pygame.image.load(f'templates/persons/{name}_{color}.png').subsurface(cords(i))
                            for i in state_images_cords]
        for i in range(len(self.stay_images)):
            self.stay_images[i] = pygame.transform.scale(self.stay_images[i], (170, 170))

        self.move_images = [pygame.image.load(f'templates/persons/{name}_{color}.png').subsurface(cords(i))
                            for i in move_images_cords[:2]]
        self.move_images = self.move_images + self.move_images
        self.move_images += [pygame.image.load(f'templates/persons/{name}_{color}.png').subsurface(cords(i))
                             for i in move_images_cords[2:4]]
        self.move_images += [pygame.image.load(f'templates/persons/{name}_{color}.png').subsurface(cords(i))
                             for i in move_images_cords[4:6]]

        for i in range(len(self.move_images)):
            self.move_images[i] = pygame.transform.scale(self.move_images[i], (170, 170))
            if i == 2 or i == 3:
                self.move_images[i] = pygame.transform.flip(self.move_images[i], True, False)

        self.img = self.stay_images[0]

    def get_big_pos(self):
        return (self.pos[0] * TILE, self.pos[1] * TILE)

    def move(self, cords):
        if self.pos != self.want_move:
            self.state = 'move_'
            cords.reverse()
            cord = cords[0]
            if self.y < cord[1] * TILE:
                self.y += 4
                self.move_to = 'D'
            elif self.y > cord[1] * TILE:
                self.y -= 4
                self.move_to = 'U'
            elif self.x < cord[0] * TILE:
                self.x += 4
                self.move_to = 'R'
            elif self.x > cord[0] * TILE:
                self.x -= 4
                self.move_to = 'L'
            else:
                self.pos = cord
                cords.reverse()
                cords.remove(cord)
                cords.reverse()
            cords.reverse()
        return cords

    def choice_image(self, tick):
        if self.pos != self.want_move:
            if self.move_to == 'L':
                self.img = self.move_images[tick % 40 // 20]
            elif self.move_to == 'R':
                self.img = self.move_images[2 + tick % 40 // 20]
            elif self.move_to == 'D':
                self.img = self.move_images[4 + tick % 40 // 20]
            elif self.move_to == 'U':
                self.img = self.move_images[6 + tick % 40 // 20]
        else:
            self.state = 'stay'
            self.move_to = ''
            if tick % 120 < 60:
                i_ = (tick % 60 // 10)
            else:
                i_ = 0
            self.img = self.stay_images[i_]
