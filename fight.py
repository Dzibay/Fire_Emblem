from settings import *
import pygame
from random import randint


# person
person_melee_attack_img = [
    pygame.image.load(f'templates/persons/roy/person/normal_attack.png').
    subsurface(124*x, 102*y, 124, 102) for y in range(0, 8) for x in range(0, 11)]
for i in range(len(person_melee_attack_img)):
    person_melee_attack_img[i] = pygame.transform.scale(person_melee_attack_img[i], (500, 500))
    person_melee_attack_img[i] = pygame.transform.flip(person_melee_attack_img[i], True, False)
person_critical_attack_img = [
    pygame.image.load(f'templates/persons/roy/person/critical_attack.png').
    subsurface(142*x, 102*y, 142, 102) for y in range(0, 8) for x in range(0, 12)]
for i in range(len(person_critical_attack_img)):
    person_critical_attack_img[i] = pygame.transform.scale(person_critical_attack_img[i], (500, 500))
    person_critical_attack_img[i] = pygame.transform.flip(person_critical_attack_img[i], True, False)

# enemy
enemy_melee_attack_img = [
    pygame.image.load(f'templates/persons/roy/enemy/normal_attack.png').
    subsurface(124 * x, 102 * y, 124, 102) for y in range(0, 8) for x in range(0, 11)]
for i in range(len(enemy_melee_attack_img)):
    enemy_melee_attack_img[i] = pygame.transform.scale(enemy_melee_attack_img[i], (500, 500))
enemy_critical_attack_img = [
    pygame.image.load(f'templates/persons/roy/enemy/critical_attack.png').
    subsurface(142 * x, 102 * y, 142, 102) for y in range(0, 8) for x in range(0, 12)]
for i in range(len(enemy_critical_attack_img)):
    enemy_critical_attack_img[i] = pygame.transform.scale(enemy_critical_attack_img[i], (500, 500))


class Fight:
    def __init__(self, person_crt=0, enemy_crt=0):
        self.moves = [True if randint(0, 100) <= person_crt else False,
                      False,
                      True if randint(0, 100) <= enemy_crt else False,
                      False]
        self.tick = 0
        self.dodge_tick = 0
        self.miss_tick = 0
        self.person_x, self.person_y = 260, 50
        self.enemy_x, self.enemy_y = 440, 50
        self.person_img_id = 0
        self.enemy_img_id = 0

        self.fight_bg = pygame.image.load('templates/fight_bg/0.png')
        self.fight_bg = pygame.transform.scale(self.fight_bg, (WIDTH, HEIGHT))

        self.miss_img = [pygame.image.load(f'templates/miss/{i}.png') for i in range(0, 12)]
        for i in range(len(self.miss_img)):
            self.miss_img[i] = pygame.transform.scale(self.miss_img[i], (100, 100))

        self.all_person_img = person_melee_attack_img + person_critical_attack_img
        self.all_enemy_img = enemy_melee_attack_img + enemy_critical_attack_img

        self.person_stay_img = person_melee_attack_img[0]
        self.enemy_stay_img = enemy_melee_attack_img[0]


        self.person_melee_attack_time = 385
        self.person_critical_attack_time = 480
        self.enemy_melee_attack_time = 385
        self.enemy_critical_attack_time = 480

    def mellee_person_attack(self):
        self.tick += 1
        img = person_melee_attack_img[self.tick % self.person_melee_attack_time // 5]

        if self.tick == self.person_melee_attack_time:
            self.tick = 0

        return img

    def critical_person_attack(self):
        self.tick += 1
        img = person_critical_attack_img[self.tick % self.person_critical_attack_time // 5]

        if self.tick == self.person_critical_attack_time:
            self.tick = 0

        return img

    def miss(self):
        self.miss_tick += 1
        if self.miss_tick < 66:
            img = self.miss_img[self.miss_tick % 66 // 6]
        else:
            img = self.miss_img[11]

        if self.miss_tick > 120:
            self.miss_tick = 0
        return img

    def mellee_enemy_attack(self):
        self.tick += 1
        img = enemy_melee_attack_img[self.tick % self.enemy_melee_attack_time // 5]

        if self.tick == self.enemy_melee_attack_time:
            self.tick = 0

        return img

    def critical_enemy_attack(self):
        self.tick += 1
        img = enemy_critical_attack_img[self.tick % self.enemy_critical_attack_time // 5]

        if self.tick == self.enemy_critical_attack_time:
            self.tick = 0

        return img
