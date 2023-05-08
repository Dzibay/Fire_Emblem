import pygame
from settings import *


def cords(c):
    return c[0], c[1], c[2], c[3]


characters = {'roy': {'hp': 18,
                      'str': 5,
                      'mag': 0,
                      'skl': 5,
                      'lck': 7,
                      'def': 5,
                      'res': 0,
                      'move': 5,
                      'class': 'sword',
                      'range': 1},

              'lyn': {'hp': 16,
                      'str': 4,
                      'mag': 0,
                      'skl': 7,
                      'lck': 5,
                      'def': 2,
                      'res': 0,
                      'move': 5,
                      'class': 'sword',
                      'range': 1},

              'hector': {'hp': 19,
                         'str': 4,
                         'mag': 1,
                         'skl': 4,
                         'lck': 3,
                         'def': 8,
                         'res': 0,
                         'move': 3,
                         'class': 'axe',
                         'range': 1},

              'eirika': {'hp': 16,
                         'str': 4,
                         'mag': 1,
                         'skl': 8,
                         'lck': 5,
                         'def': 3,
                         'res': 1,
                         'move': 6,
                         'class': 'lance',
                         'range': 1},

              'eliwood': {'hp': 18,
                          'str': 5,
                          'mag': 5,
                          'skl': 5,
                          'lck': 7,
                          'def': 5,
                          'res': 0,
                          'move': 6,
                          'class': 'sword',
                          'range': 1},

              'marth': {'hp': 18,
                        'str': 5,
                        'mag': 0,
                        'skl': 3,
                        'lck': 7,
                        'def': 7,
                        'res': 7,
                        'move': 4,
                        'class': 'sword',
                        'range': 1},

              'ike': {'hp': 20,
                      'str': 4,
                      'mag': 5,
                      'skl': 5,
                      'lck': 6,
                      'def': 7,
                      'res': 6,
                      'move': 4,
                      'class': 'sword',
                      'range': 1},

              'sorcerer': {'hp': 15,
                           'str': 1,
                           'mag': 18,
                           'skl': 4,
                           'lck': 4,
                           'def': 0,
                           'res': 3,
                           'move': 3,
                           'class': 'magic',
                           'range': 2}}

weapon_damage = {'sword': 5, 'axe': 8, 'lance': 7, 'magic': 5}


class Person:
    def __init__(self, x, y, name):
        print('person')
        self.x = x
        self.y = y
        self.name = name
        self.state = 'stay'
        self.pos = (self.x // TILE, self.y // TILE)
        self.want_move = self.pos
        self.move_to = ''
        self.damage_for_me = 0

        self.type = characters[self.name]['class']
        self.weapon_dmg = weapon_damage[self.type]
        self.hp = characters[self.name]['hp']
        self.max_hp = self.hp
        self.hit = 90
        self.str = characters[self.name]['str']
        self.mag = characters[self.name]['mag']
        self.skl = characters[self.name]['skl']
        self.lck = characters[self.name]['lck']
        self.def_ = characters[self.name]['def']
        self.res = characters[self.name]['res']
        self.movement = characters[self.name]['move']
        self.range_attack = characters[self.name]['range']

        self.dmg = self.mag if self.type == 'magic' else (self.str + 5)
        self.crt = self.skl // 2 + 1

        self.can_fight_with = []
        self.attack_button = None

        # person
        self.stay_images = [pygame.transform.scale(pygame.image.load(f'templates/persons/{name}/person/map_idle.png').
                                                   subsurface((i * 48, 0, 48, 48)), (250, 250)) for i in range(4)] + \
                           [pygame.transform.scale(
                               pygame.image.load(f'templates/persons/{name}/person/map_selected.png').
                               subsurface((i * 48, 0, 48, 48)), (250, 250)) for i in range(4)]
        self.move_up_images = [pygame.transform.scale(pygame.image.load(f'templates/persons/{name}/person/map_up.png').
                                                      subsurface((i * 48, 0, 48, 48)), (250, 250)) for i in range(4)]
        self.move_down_images = [
            pygame.transform.scale(pygame.image.load(f'templates/persons/{name}/person/map_down.png').
                                   subsurface((i * 48, 0, 48, 48)), (250, 250)) for i in range(4)]
        self.move_left_images = [
            pygame.transform.scale(pygame.image.load(f'templates/persons/{name}/person/map_side.png').
                                   subsurface((i * 48, 0, 48, 48)), (250, 250)) for i in range(4)]
        self.move_right_images = [pygame.transform.flip(i, True, False) for i in self.move_left_images]
        self.img = self.stay_images[0]

        # enemy
        self.enemy_stay_images = [
            pygame.transform.scale(pygame.image.load(f'templates/persons/{name}/enemy/map_idle.png').
                                   subsurface((i * 48, 0, 48, 48)), (250, 250)) for i in range(4)]
        self.enemy_move_up_images = [
            pygame.transform.scale(pygame.image.load(f'templates/persons/{name}/enemy/map_up.png').
                                   subsurface((i * 48, 0, 48, 48)), (250, 250)) for i in range(4)]
        self.enemy_move_down_images = [
            pygame.transform.scale(pygame.image.load(f'templates/persons/{name}/enemy/map_down.png').
                                   subsurface((i * 48, 0, 48, 48)), (250, 250)) for i in range(4)]
        self.enemy_move_left_images = [
            pygame.transform.scale(pygame.image.load(f'templates/persons/{name}/enemy/map_side.png').
                                   subsurface((i * 48, 0, 48, 48)), (250, 250)) for i in range(4)]
        self.enemy_move_right_images = [
            pygame.transform.flip(i, True, False) for i in self.move_left_images]

    def get_big_pos(self):
        return (self.pos[0] * TILE, self.pos[1] * TILE)

    def move(self, cords):
        if self.pos != self.want_move:
            self.state = 'move_'
            cords.reverse()
            cord = cords[0]
            if self.y < cord[1] * TILE:
                self.y += 8
                self.move_to = 'D'
            elif self.y > cord[1] * TILE:
                self.y -= 8
                self.move_to = 'U'
            elif self.x < cord[0] * TILE:
                self.x += 8
                self.move_to = 'R'
            elif self.x > cord[0] * TILE:
                self.x -= 8
                self.move_to = 'L'
            else:
                self.pos = cord
                cords.reverse()
                cords.remove(cord)
                cords.reverse()
            cords.reverse()
        return cords

    def choice_image(self, tick, choice):
        if self.pos != self.want_move:
            if self.move_to == 'L':
                self.img = self.move_left_images[tick % 40 // 10]
            elif self.move_to == 'R':
                self.img = self.move_right_images[tick % 40 // 10]
            elif self.move_to == 'D':
                self.img = self.move_down_images[tick % 40 // 10]
            elif self.move_to == 'U':
                self.img = self.move_up_images[tick % 40 // 10]
        else:
            self.state = 'stay'
            self.move_to = ''
            if tick % 120 < 40:
                i_ = (tick % 40 // 10) + (4 if choice else 0)
            else:
                i_ = 0

            self.img = self.stay_images[i_]
