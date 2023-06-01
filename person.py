import pygame
from settings import *
from data.persons import characters
from weapon import Weapon
from random import randint


def cords(c):
    return c[0], c[1], c[2], c[3]


class Person:
    def __init__(self, x, y, name, lvl, choice_weapon=None):
        print('person')
        self.x = x
        self.y = y
        self.name = name
        self.state = 'stay'
        self.pos = (self.x // TILE, self.y // TILE)
        self.want_move = self.pos
        self.move_to = ''
        self.damage_for_me = 0

        # stats
        self.lvl = lvl
        self.weapon = Weapon(choice_weapon if choice_weapon is not None else characters[self.name]['weapon'])
        self.hp = characters[self.name]['hp']
        self.max_hp = self.hp
        self.str = characters[self.name]['str']
        self.mag = characters[self.name]['mag']
        self.skl = characters[self.name]['skl']
        self.lck = characters[self.name]['lck']
        self.def_ = characters[self.name]['def']
        self.res = characters[self.name]['res']
        self.con = characters[self.name]['con']
        self.movement = characters[self.name]['move']
        self.speed = characters[self.name]['speed']
        self.class_ = characters[self.name]['class']
        if self.lvl > 1:
            self.change_lvl()

        self.bonus_characters_from_weapon(self.weapon.name, False)

        self.hit = self.weapon.hit + (self.skl * 2) + (self.lck // 2)
        self.dmg = (self.mag if self.weapon.class_ == 'magic' else self.str) + self.weapon.mt
        self.crt = self.weapon.crt + (self.skl // 2)
        self.attack_speed = self.speed - (self.weapon.wt - self.con if self.weapon.wt - self.con > 0 else 0)
        self.avoid = self.attack_speed * 2 + self.lck

        # images
        self.map_images = {'person': {},
                           'enemy': {}}
        for person in self.map_images:
            self.map_images[person]['stand'] = [
                pygame.transform.scale(pygame.image.load(f'templates/persons/{self.name}/{person}/stand.png').
                                       subsurface((i*64, 0, 64, 48)), (350, 260)) for i in range(3)]
            self.map_images[person]['passive'] = [
                pygame.transform.scale(pygame.image.load(f'templates/persons/{self.name}/{person}/stand.png').
                                       subsurface((i*64, 48, 64, 48)), (350, 260)) for i in range(3)]
            self.map_images[person]['active'] = [
                pygame.transform.scale(pygame.image.load(f'templates/persons/{self.name}/{person}/stand.png').
                                       subsurface((i*64, 96, 64, 48)), (350, 260)) for i in range(3)]

            self.map_images[person]['down'] = [
                pygame.transform.scale(pygame.image.load(f'templates/persons/{self.name}/{person}/move.png').
                                       subsurface((i*48, 0, 48, 40)), (260, 215)) for i in range(4)]
            self.map_images[person]['left'] = [
                pygame.transform.scale(pygame.image.load(f'templates/persons/{self.name}/{person}/move.png').
                                       subsurface((i*48, 40, 48, 40)), (260, 215)) for i in range(4)]
            self.map_images[person]['right'] = [
                pygame.transform.scale(pygame.image.load(f'templates/persons/{self.name}/{person}/move.png').
                                       subsurface((i*48, 80, 48, 40)), (260, 215)) for i in range(4)]
            self.map_images[person]['up'] = [
                pygame.transform.scale(pygame.image.load(f'templates/persons/{self.name}/{person}/move.png').
                                       subsurface((i*48, 120, 48, 40)), (260, 215)) for i in range(4)]
        self.img = self.map_images['person']['stand'][0]

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
        self.crt = self.weapon.crt + (self.skl // 2)
        self.hit = self.weapon.hit + (self.skl * 2) + (self.lck // 2)
        self.dmg = (self.mag if self.weapon.class_ == 'magic' else self.str) + self.weapon.mt

    def change_lvl(self):
        for i in range(self.lvl - 1):
            self.hp += 1 if randint(0, 100) < characters[self.name]['rates']['hp'] else 0
            if self.weapon.class_ == 'magic':
                self.mag += 1 if randint(0, 100) < characters[self.name]['rates']['mag'] else 0
            else:
                self.str += 1 if randint(0, 100) < characters[self.name]['rates']['str'] else 0
            self.skl += 1 if randint(0, 100) < characters[self.name]['rates']['skl'] else 0
            self.speed += 1 if randint(0, 100) < characters[self.name]['rates']['speed'] else 0
            self.lck += 1 if randint(0, 100) < characters[self.name]['rates']['lck'] else 0
            self.def_ += 1 if randint(0, 100) < characters[self.name]['rates']['def'] else 0
            self.res += 1 if randint(0, 100) < characters[self.name]['rates']['res'] else 0
        self.max_hp = self.hp

    def get_big_pos(self):
        return (self.pos[0] * TILE, self.pos[1] * TILE)

    def move(self, cords):
        if self.pos != self.want_move:
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
                cords.reverse()
                cords.remove(cord)
                cords.reverse()
            cords.reverse()
        return cords

    def choice_image(self, tick, choice):
        if self.pos != self.want_move and self.move_to != '':
            self.img = self.map_images['person'][self.move_to][tick % 40 // 10]

        else:
            self.state = 'stay'
            self.move_to = ''

            self.img = self.map_images['person']['active' if choice else 'stand'][
                tick % 30 // 10 if tick % 120 < 40 else 0]
