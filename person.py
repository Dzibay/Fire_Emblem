import pygame
from settings import *
from data.persons import characters
from weapon import Weapon
from map.generate_map import lvl_generate, def_buff, avoid_buff
from data.classes import types


lords = ['roy', 'lyn', 'marth', 'ike', 'eirika', 'eliwood', 'hector', 'ephraim']


def cords(c):
    return c[0], c[1], c[2], c[3]


class Person:
    def __init__(self, x, y, name, stats, choice_weapon=None):
        print('person')
        self.x = x
        self.y = y
        self.name = name
        self.state = 'stay'
        self.pos = (self.x // TILE, self.y // TILE)
        self.terra_pos = lvl_generate[self.pos]
        self.last_terra_pos = self.terra_pos
        self.want_move = self.pos
        self.move_to = ''
        self.damage_for_me = 0
        self.active = True
        self.gender = characters[self.name]['gender']

        # stats
        self.lvl = stats['lvl']
        self.hp = stats['hp']
        self.str = stats['str']
        self.mag = stats['mag']
        self.skl = stats['skl']
        self.lck = stats['lck']
        self.def_ = stats['def']
        self.res = stats['res']
        self.con = stats['con']
        self.speed = stats['speed']
        self.movement = stats['move']
        self.class_ = stats['class']

        self.flying = True if self.class_ in types['flying'] else False

        self.max_hp = self.hp
        self.weapon = Weapon(choice_weapon if choice_weapon is not None else characters[self.name]['weapon'])

        self.bonus_characters_from_weapon(self.weapon.name, False)

        self.hit = self.weapon.hit + (self.skl * 2) + (self.lck // 2)
        self.dmg = (self.mag if self.weapon.class_ == 'magic' else self.str) + self.weapon.mt
        self.crt = self.weapon.crt + (self.skl // 2)
        self.attack_speed = self.speed - (self.weapon.wt - self.con if self.weapon.wt - self.con > 0 else 0)
        if self.attack_speed < 0:
            self.attack_speed = 0
        self.avoid = self.attack_speed * 2 + self.lck

        if self.name in lords:
            # images
            t_ = 'T1' if self.lvl < 10 else 'T2'
            self.map_images = {weapon_: {'person': {}, 'enemy': {}} for weapon_ in
                               characters[self.name]['can_use' if self.lvl < 10 else 't2_can_use']}
            for weapon_ in self.map_images:
                for person in self.map_images[weapon_]:
                    self.map_images[weapon_][person]['stand'] = []
                    for i in range(3):
                        image = pygame.transform.scale(pygame.image.load(f'templates/persons/lords/{self.name}/map/{t_}/{weapon_}/{person}/stand.png').convert_alpha().subsurface((i * 64, 0, 64, 48)), (350, 260))
                        trans_color = image.get_at((0, 0))
                        image.set_colorkey(trans_color)
                        self.map_images[weapon_][person]['stand'].append(image)

                    self.map_images[weapon_][person]['passive'] = []
                    for i in range(3):
                        image = pygame.transform.scale(pygame.image.load(f'templates/persons/lords/{self.name}/map/{t_}/{weapon_}/{person}/stand.png').convert_alpha().subsurface((i * 64, 48, 64, 48)), (350, 260))
                        trans_color = image.get_at((0, 0))
                        image.set_colorkey(trans_color)
                        self.map_images[weapon_][person]['passive'].append(image)

                    self.map_images[weapon_][person]['active'] = []
                    for i in range(3):
                        image = pygame.transform.scale(pygame.image.load(f'templates/persons/lords/{self.name}/map/{t_}/{weapon_}/{person}/stand.png').convert_alpha().subsurface((i * 64, 96, 64, 48)), (350, 260))
                        trans_color = image.get_at((0, 0))
                        image.set_colorkey(trans_color)
                        self.map_images[weapon_][person]['active'].append(image)

                    self.map_images[weapon_][person]['down'] = []
                    for i in range(4):
                        image = pygame.transform.scale(pygame.image.load(f'templates/persons/lords/{self.name}/map/{t_}/{weapon_}/{person}/move.png').convert_alpha().subsurface((i * 48, 0, 48, 40)), (260, 215))
                        trans_color = image.get_at((0, 0))
                        image.set_colorkey(trans_color)
                        self.map_images[weapon_][person]['down'].append(image)

                    self.map_images[weapon_][person]['left'] = []
                    for i in range(4):
                        image = pygame.transform.scale(pygame.image.load(f'templates/persons/lords/{self.name}/map/{t_}/{weapon_}/{person}/move.png').convert_alpha().subsurface((i * 48, 40, 48, 40)), (260, 215))
                        trans_color = image.get_at((0, 0))
                        image.set_colorkey(trans_color)
                        self.map_images[weapon_][person]['left'].append(image)

                    self.map_images[weapon_][person]['right'] = []
                    for i in range(4):
                        image = pygame.transform.scale(pygame.image.load(f'templates/persons/lords/{self.name}/map/{t_}/{weapon_}/{person}/move.png').convert_alpha().subsurface((i * 48, 80, 48, 40)), (260, 215))
                        trans_color = image.get_at((0, 0))
                        image.set_colorkey(trans_color)
                        self.map_images[weapon_][person]['right'].append(image)

                    self.map_images[weapon_][person]['up'] = []
                    for i in range(4):
                        image = pygame.transform.scale(pygame.image.load(f'templates/persons/lords/{self.name}/map/{t_}/{weapon_}/{person}/move.png').convert_alpha().subsurface((i * 48, 120, 48, 40)), (260, 215))
                        trans_color = image.get_at((0, 0))
                        image.set_colorkey(trans_color)
                        self.map_images[weapon_][person]['up'].append(image)
        else:
            self.map_images = {weapon_: {'person': {}, 'enemy': {}} for weapon_ in characters[self.name]['can_use' if self.lvl < 10 else 't2_can_use']}
            try:
                for weapon_ in self.map_images:
                    for person in self.map_images[weapon_]:
                        self.map_images[weapon_][person]['stand'] = []
                        for i in range(3):
                            image = pygame.transform.scale(pygame.image.load(
                                f'templates/persons/other/{self.class_}/{self.name}/map/{weapon_}/{person}/stand.png').convert_alpha().subsurface(
                                (i * 64, 0, 64, 48)), (350, 260))
                            trans_color = image.get_at((0, 0))
                            image.set_colorkey(trans_color)
                            self.map_images[weapon_][person]['stand'].append(image)

                        self.map_images[weapon_][person]['passive'] = []
                        for i in range(3):
                            image = pygame.transform.scale(pygame.image.load(
                                f'templates/persons/other/{self.class_}/{self.name}/map/{weapon_}/{person}/stand.png').convert_alpha().subsurface(
                                (i * 64, 48, 64, 48)), (350, 260))
                            trans_color = image.get_at((0, 0))
                            image.set_colorkey(trans_color)
                            self.map_images[weapon_][person]['passive'].append(image)

                        self.map_images[weapon_][person]['active'] = []
                        for i in range(3):
                            image = pygame.transform.scale(pygame.image.load(
                                f'templates/persons/other/{self.class_}/{self.name}/map/{weapon_}/{person}/stand.png').convert_alpha().subsurface(
                                (i * 64, 96, 64, 48)), (350, 260))
                            trans_color = image.get_at((0, 0))
                            image.set_colorkey(trans_color)
                            self.map_images[weapon_][person]['active'].append(image)

                        self.map_images[weapon_][person]['down'] = []
                        for i in range(4):
                            image = pygame.transform.scale(pygame.image.load(
                                f'templates/persons/other/{self.class_}/{self.name}/map/{weapon_}/{person}/move.png').convert_alpha().subsurface(
                                (i * 48, 0, 48, 40)), (260, 215))
                            trans_color = image.get_at((0, 0))
                            image.set_colorkey(trans_color)
                            self.map_images[weapon_][person]['down'].append(image)

                        self.map_images[weapon_][person]['left'] = []
                        for i in range(4):
                            image = pygame.transform.scale(pygame.image.load(
                                f'templates/persons/other/{self.class_}/{self.name}/map/{weapon_}/{person}/move.png').convert_alpha().subsurface(
                                (i * 48, 40, 48, 40)), (260, 215))
                            trans_color = image.get_at((0, 0))
                            image.set_colorkey(trans_color)
                            self.map_images[weapon_][person]['left'].append(image)

                        self.map_images[weapon_][person]['right'] = []
                        for i in range(4):
                            image = pygame.transform.scale(pygame.image.load(
                                f'templates/persons/other/{self.class_}/{self.name}/map/{weapon_}/{person}/move.png').convert_alpha().subsurface(
                                (i * 48, 80, 48, 40)), (260, 215))
                            trans_color = image.get_at((0, 0))
                            image.set_colorkey(trans_color)
                            self.map_images[weapon_][person]['right'].append(image)

                        self.map_images[weapon_][person]['up'] = []
                        for i in range(4):
                            image = pygame.transform.scale(pygame.image.load(
                                f'templates/persons/other/{self.class_}/{self.name}/map/{weapon_}/{person}/move.png').convert_alpha().subsurface(
                                (i * 48, 120, 48, 40)), (260, 215))
                            trans_color = image.get_at((0, 0))
                            image.set_colorkey(trans_color)
                            self.map_images[weapon_][person]['up'].append(image)
            except:
                for weapon_ in self.map_images:
                    for person in self.map_images[weapon_]:
                        self.map_images[weapon_][person]['stand'] = []
                        for i in range(3):
                            image = pygame.transform.scale(pygame.image.load(
                                f'templates/persons/other/{self.class_}/{self.gender}/map/{weapon_}/{person}/stand.png').convert_alpha().subsurface(
                                (i * 64, 0, 64, 48)), (350, 260))
                            trans_color = image.get_at((0, 0))
                            image.set_colorkey(trans_color)
                            self.map_images[weapon_][person]['stand'].append(image)

                        self.map_images[weapon_][person]['passive'] = []
                        for i in range(3):
                            image = pygame.transform.scale(pygame.image.load(
                                f'templates/persons/other/{self.class_}/{self.gender}/map/{weapon_}/{person}/stand.png').convert_alpha().subsurface(
                                (i * 64, 48, 64, 48)), (350, 260))
                            trans_color = image.get_at((0, 0))
                            image.set_colorkey(trans_color)
                            self.map_images[weapon_][person]['passive'].append(image)

                        self.map_images[weapon_][person]['active'] = []
                        for i in range(3):
                            image = pygame.transform.scale(pygame.image.load(
                                f'templates/persons/other/{self.class_}/{self.gender}/map/{weapon_}/{person}/stand.png').convert_alpha().subsurface(
                                (i * 64, 96, 64, 48)), (350, 260))
                            trans_color = image.get_at((0, 0))
                            image.set_colorkey(trans_color)
                            self.map_images[weapon_][person]['active'].append(image)

                        self.map_images[weapon_][person]['down'] = []
                        for i in range(4):
                            image = pygame.transform.scale(pygame.image.load(
                                f'templates/persons/other/{self.class_}/{self.gender}/map/{weapon_}/{person}/move.png').convert_alpha().subsurface(
                                (i * 48, 0, 48, 40)), (260, 215))
                            trans_color = image.get_at((0, 0))
                            image.set_colorkey(trans_color)
                            self.map_images[weapon_][person]['down'].append(image)

                        self.map_images[weapon_][person]['left'] = []
                        for i in range(4):
                            image = pygame.transform.scale(pygame.image.load(
                                f'templates/persons/other/{self.class_}/{self.gender}/map/{weapon_}/{person}/move.png').convert_alpha().subsurface(
                                (i * 48, 40, 48, 40)), (260, 215))
                            trans_color = image.get_at((0, 0))
                            image.set_colorkey(trans_color)
                            self.map_images[weapon_][person]['left'].append(image)

                        self.map_images[weapon_][person]['right'] = []
                        for i in range(4):
                            image = pygame.transform.scale(pygame.image.load(
                                f'templates/persons/other/{self.class_}/{self.gender}/map/{weapon_}/{person}/move.png').convert_alpha().subsurface(
                                (i * 48, 80, 48, 40)), (260, 215))
                            trans_color = image.get_at((0, 0))
                            image.set_colorkey(trans_color)
                            self.map_images[weapon_][person]['right'].append(image)

                        self.map_images[weapon_][person]['up'] = []
                        for i in range(4):
                            image = pygame.transform.scale(pygame.image.load(
                                f'templates/persons/other/{self.class_}/{self.gender}/map/{weapon_}/{person}/move.png').convert_alpha().subsurface(
                                (i * 48, 120, 48, 40)), (260, 215))
                            trans_color = image.get_at((0, 0))
                            image.set_colorkey(trans_color)
                            self.map_images[weapon_][person]['up'].append(image)
        self.img = self.map_images[self.weapon.class_]['person']['stand'][0]

    def bonus_characters_from_weapon(self, new_weapon, characters_down=True):
        if characters_down:
            if self.weapon.name == 'durandal':
                self.str -= 5
            elif self.weapon.name == 'armads':
                self.def_ -= 5
            elif self.weapon.name == 'sol_katti':
                self.def_ -= 5

        if new_weapon == 'durandal':
            self.str += 5
        elif new_weapon == 'armads':
            self.def_ += 5
        elif new_weapon == 'sol_katti':
            self.def_ += 5

    def change_weapon(self, weapon_to_change):
        self.bonus_characters_from_weapon(weapon_to_change)
        self.weapon = Weapon(weapon_to_change)
        self.attack_speed = characters[self.name]['speed'] - (self.weapon.wt - self.con
                                                              if self.weapon.wt - self.con > 0 else 0)
        if self.attack_speed < 0:
            self.attack_speed = 0
        self.crt = self.weapon.crt + (self.skl // 2)
        self.hit = self.weapon.hit + (self.skl * 2) + (self.lck // 2)
        self.dmg = (self.mag if self.weapon.class_ == 'magic' else self.str) + self.weapon.mt

    def get_big_pos(self):
        return (self.pos[0] * TILE, self.pos[1] * TILE)

    def move(self, cords, terra=False):
        self.state = ''
        cords.reverse()
        cord = cords[0]
        if self.y < cord[1] * TILE:
            self.y += 8
            self.move_to = 'down'
        elif self.y > cord[1] * TILE:
            self.y -= 8
            self.move_to = 'up'
        elif self.x < cord[0] * TILE:
            self.x += 8
            self.move_to = 'right'
        elif self.x > cord[0] * TILE:
            self.x -= 8
            self.move_to = 'left'
        else:
            self.pos = cord
            self.terra_pos = lvl_generate[self.pos]
            cords.reverse()
            cords.remove(cord)
            cords.reverse()
        cords.reverse()

        if terra:
            self.def_ -= def_buff[self.last_terra_pos]
            self.avoid -= avoid_buff[self.last_terra_pos]

            self.def_ += def_buff[self.terra_pos]
            self.avoid += avoid_buff[self.terra_pos]

            self.last_terra_pos = self.terra_pos
        return cords

    def choice_image(self, tick, choice):
        if self.pos != self.want_move and self.move_to != '':
            self.img = self.map_images[self.weapon.class_]['person'][self.move_to][tick % 40 // 10]

        else:
            self.state = 'stay'
            self.move_to = ''
            if self.active:
                p_ = 'active' if choice else 'stand'
            else:
                p_ = 'passive'
            self.img = self.map_images[self.weapon.class_]['person'][p_][tick % 15 // 5 if tick % 60 <= 15 else 0]
