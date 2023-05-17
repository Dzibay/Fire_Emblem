from settings import *
import pygame
from random import randint
from data.fight_sprites_characters import sizes
from data.weapon import weapon_img, weapon_arrow


magic = {
    'flux': {'width': 65,
             'height': 99,
             'w': 5,
             'h': 7,
             'frames': 35,
             'x': 600,
             'y': 85,
             'x1': 260},

    'fire': {'width': 65,
             'height': 99,
             'w': 5,
             'h': 7,
             'frames': 35,
             'x': 600,
             'y': 85,
             'x1': 250}
}

magic_names = ['sorcerer', 'sagem']


def triangle(weapon_1, weapon_2):
    if weapon_1 == weapon_2:
        return False
    elif weapon_1 == 'sword':
        if weapon_2 == 'axe':
            return True
        elif weapon_2 == 'lance':
            return False
    elif weapon_1 == 'axe':
        if weapon_2 == 'lance':
            return True
        elif weapon_2 == 'sword':
            return False
    elif weapon_1 == 'lance':
        if weapon_2 == 'sword':
            return True
        elif weapon_2 == 'axe':
            return False
    elif weapon_1 == 'bow':
        return False
    elif weapon_2 == 'bow' and weapon_1 != 'magic':
        return True


class Fight_images:
    def __init__(self):
        self.images = {}
        self.magic_effects = {}
        self.upload_images = False

    def uppload_images(self, names):
        for name in names:
            if name not in self.images:
                if name in magic_names and not self.upload_images:
                    self.upload_images = True
                    # magic
                    for magic_ in ['flux']:
                        self.magic_effects[magic_] = {'person': [], 'enemy': []}
                        # enemy magic
                        self.magic_effects[magic_]['enemy'] = [pygame.transform.scale(
                            pygame.image.load(f'templates/magic/{magic_}.png').
                            subsurface(x * magic[f'{magic_}']['width'], y * magic[f'{magic_}']['height'],
                                       magic[f'{magic_}']['width'], magic[f'{magic_}']['height']), (290, 450))
                                                                           for y in range(magic[f'{magic_}']['h'])
                                                                           for x in range(magic[f'{magic_}']['w'])][
                                                                       :magic[f'{magic_}']['frames']]

                        # person magic
                        self.magic_effects[magic_]['person'] = [pygame.transform.flip(i, True, False)
                                                                for i in self.magic_effects[magic_]['enemy']]

                # persons
                self.images[name] = {weapon: {'person': {'norm': [], 'crt': []}, 'enemy': {'norm': [], 'crt': []}}
                                     for weapon in ['sword', 'axe', 'lance', 'bow', 'magic']}
                for weapon in ['sword', 'axe', 'lance', 'bow', 'magic']:
                    self.images[name][weapon] = {'person': {'norm': [], 'crt': []}, 'enemy': {'norm': [], 'crt': []}}
                    # enemy

                    try:
                        enemy_melee_attack_img = [pygame.image.load(
                            f'templates/persons/{name}/{weapon}/normal_attack.png').
                                                  subsurface(sizes[name][weapon][0]['width'] * x,
                                                             sizes[name][weapon][0]['height'] * y,
                                                             sizes[name][weapon][0]['width'],
                                                             sizes[name][weapon][0]['height'])
                                                  for y in range(0, sizes[name][weapon][0]['h'])
                                                  for x in range(0, sizes[name][weapon][0]['w'])][
                                                 :sizes[name][weapon][0]['frames']]
                        for i in range(len(enemy_melee_attack_img)):
                            enemy_melee_attack_img[i] = pygame.transform.scale(enemy_melee_attack_img[i],
                                                                               sizes[name][weapon][0]['size'])
                    except:
                        enemy_melee_attack_img = []

                    try:
                        enemy_critical_attack_img = [pygame.image.load(
                            f'templates/persons/{name}/{weapon}/critical_attack.png').
                                                     subsurface(sizes[name][weapon][1]['width'] * x,
                                                                sizes[name][weapon][1]['height'] * y,
                                                                sizes[name][weapon][1]['width'],
                                                                sizes[name][weapon][1]['height'])
                                                     for y in range(0, sizes[name][weapon][1]['h'])
                                                     for x in range(0, sizes[name][weapon][1]['w'])][
                                                    :sizes[name][weapon][1]['frames']]
                        for i in range(len(enemy_critical_attack_img)):
                            enemy_critical_attack_img[i] = pygame.transform.scale(enemy_critical_attack_img[i],
                                                                                  sizes[name][weapon][1]['size'])
                    except:
                        enemy_critical_attack_img = []

                    # person
                    person_melee_attack_img = [pygame.transform.flip(img, True, False) for img in
                                               enemy_melee_attack_img]
                    person_critical_attack_img = [pygame.transform.flip(img, True, False) for img in
                                                  enemy_critical_attack_img]

                    self.images[name][weapon]['person']['norm'] = person_melee_attack_img
                    self.images[name][weapon]['person']['crt'] = person_critical_attack_img
                    self.images[name][weapon]['enemy']['norm'] = enemy_melee_attack_img
                    self.images[name][weapon]['enemy']['crt'] = enemy_critical_attack_img


class Fight:
    def __init__(self, person, enemy, fight_images, person_dmg=0, enemy_dmg=0):
        self.person_hit = person.hit + (15 if triangle(person.type, enemy.type) else -15) - enemy.avoid
        self.enemy_hit = enemy.hit + (15 if triangle(enemy.type, person.type) else -15) - person.avoid
        self.moves = [True if randint(0, 100) <= person.crt else False,
                      True if randint(0, 100) <= (100 - self.person_hit) else False,
                      True if randint(0, 100) <= enemy.crt else False,
                      True if randint(0, 100) <= (100 - self.enemy_hit) else False]
        print(self.moves)
        # self.moves = [True, False, False, False]

        self.without_enemy_attack = False
        self.person_double_attack = False
        self.enemy_double_attack = False
        self.indicate_double_attack = False
        self.distance_fight = False
        range_persons = abs(person.pos[0] - enemy.pos[0]) + abs(person.pos[1] - enemy.pos[1])
        if range_persons not in enemy.range_attack:
            self.without_enemy_attack = True
        if person.attack_speed - enemy.attack_speed >= 4:
            self.person_double_attack = True
            self.moves.append(True if randint(0, 100) <= (1 - person.hit) else False)
        elif enemy.attack_speed - person.attack_speed >= 4:
            self.enemy_double_attack = True
            self.moves.append(True if randint(0, 100) <= enemy.crt else False)
            self.moves.append(True if randint(0, 100) <= (1 - enemy.hit) else False)
        if range_persons > 1:
            self.distance_fight = True

        self.need_moves = [0, 0]
        self.tick = 0
        self.dodge_tick = 0
        self.miss_tick = 0
        self.magic_tick = 0

        # weapon
        self.person_weapon_img = weapon_img[person.weapon]
        self.enemy_weapon_img = weapon_img[enemy.weapon]

        self.person_x, self.person_y = sizes[person.name][person.type][int(self.moves[0])]['x'], \
                                       sizes[person.name][person.type][int(self.moves[0])]['y']
        self.enemy_x, self.enemy_y = sizes[enemy.name][enemy.type][int(self.moves[2])]['x1'], \
                                     sizes[enemy.name][enemy.type][int(self.moves[2])]['y']
        if self.distance_fight:
            self.person_x -= 200
            self.enemy_x += 200
        self.person_dmg_tick = sizes[enemy.name][enemy.type][int(self.moves[2])]['dmg_time']
        self.enemy_dmg_tick = sizes[person.name][person.type][int(self.moves[0])]['dmg_time']
        self.person_dmg = person_dmg
        self.enemy_dmg = enemy_dmg
        self.person_img_id = 0
        self.enemy_img_id = 0
        self.person_weapon_arrow = weapon_arrow['up' if triangle(person.type, enemy.type) else 'down']
        self.enemy_weapon_arrow = weapon_arrow['up' if triangle(enemy.type, person.type) else 'down']

        # magic
        self.magic_img_id = -1
        self.person_magic_cords = (1, 1)
        self.person_magic_cords_sms = (1, 1)
        self.enemy_magic_cords = (1, 1)
        self.enemy_magic_cords_sms = (1, 1)
        self.person_magic_effect = []
        self.enemy_magic_effect = []

        if person.type == 'magic':
            self.person_magic_cords = (magic[person.weapon]['x'], magic[person.weapon]['y'])
            self.person_magic_cords_sms = (magic[person.weapon]['x1'], magic[person.weapon]['y'])

            self.person_magic_effect = fight_images.magic_effects[person.weapon]['person']
            self.person_magic_effect_time = len(self.person_magic_effect) * 2

        if enemy.type == 'magic':
            self.enemy_magic_cords = (magic[enemy.weapon]['x1'], magic[enemy.weapon]['y'])
            self.enemy_magic_cords_sms = (magic[enemy.weapon]['x'], magic[enemy.weapon]['y'])

            self.enemy_magic_effect = fight_images.magic_effects[enemy.weapon]['enemy']
            self.enemy_magic_effect_time = len(self.enemy_magic_effect) * 2

        self.all_effects = self.person_magic_effect + self.enemy_magic_effect

        if self.distance_fight:
            if self.person_magic_cords != (0, 0):
                self.person_magic_cords = (self.person_magic_cords[0] + 200, self.person_magic_cords[1])
                self.person_magic_cords_sms = (self.person_magic_cords_sms[0] - 200, self.person_magic_cords_sms[1])
            if self.enemy_magic_cords != (0, 0):
                self.enemy_magic_cords = (self.enemy_magic_cords[0] - 200, self.enemy_magic_cords[1])
                self.enemy_magic_cords_sms = (self.enemy_magic_cords_sms[0] + 200, self.enemy_magic_cords_sms[1])

        # baze
        self.fight_bg = pygame.image.load('templates/fight/bg.png').subsurface(1, 1, 240, 160)
        if self.distance_fight:
            self.fight_characters = pygame.image.load('templates/fight/distance_baze.png')
        else:
            self.fight_characters = pygame.image.load('templates/fight/baze.png')
        self.fight_bg = pygame.transform.scale(self.fight_bg, (WIDTH, HEIGHT))
        self.fight_characters = pygame.transform.scale(self.fight_characters, (WIDTH, HEIGHT))
        self.numbers = [pygame.transform.scale(
            pygame.image.load('templates/fight/numbers.png').subsurface(i * 8, 0, 8, 8), (40, 40)) for i in range(10)]
        self.hp = [pygame.transform.scale(
            pygame.image.load('templates/fight/hp.png').subsurface(i * 2, 0, 2, 7), (10, 35)) for i in range(2)]

        self.miss_img = [pygame.image.load(f'templates/miss/{i}.png') for i in range(0, 12)]
        for i in range(len(self.miss_img)):
            self.miss_img[i] = pygame.transform.scale(self.miss_img[i], (100, 100))

        # persons
        self.person_melee_attack_img = fight_images.images[person.name][person.type]['person']['norm']
        self.person_critical_attack_img = fight_images.images[person.name][person.type]['person']['crt']
        self.all_person_img = self.person_melee_attack_img + self.person_critical_attack_img
        self.enemy_melee_attack_img = fight_images.images[enemy.name][enemy.type]['enemy']['norm']
        self.enemy_critical_attack_img = fight_images.images[enemy.name][enemy.type]['enemy']['crt']
        self.all_enemy_img = self.enemy_melee_attack_img + self.enemy_critical_attack_img

        self.person_stay_img = self.person_critical_attack_img[0] if self.moves[0] else self.person_melee_attack_img[0]
        self.enemy_stay_img = self.enemy_critical_attack_img[0] if self.moves[2] else self.enemy_melee_attack_img[0]

        # attack time
        self.person_melee_attack_time = len(self.person_melee_attack_img) * 2
        self.person_critical_attack_time = len(self.person_critical_attack_img) * 2
        self.enemy_melee_attack_time = len(self.enemy_melee_attack_img) * 2
        self.enemy_critical_attack_time = len(self.enemy_critical_attack_img) * 2

    def mellee_person_attack(self):
        self.tick += 1
        img = self.person_melee_attack_img[self.tick % self.person_melee_attack_time // 2]

        if self.tick == self.person_melee_attack_time:
            self.tick = 0

        return img

    def critical_person_attack(self):
        self.tick += 1
        img = self.person_critical_attack_img[self.tick % self.person_critical_attack_time // 2]

        if self.tick == self.person_critical_attack_time:
            self.tick = 0

        return img

    def miss(self):
        self.miss_tick += 1
        if self.miss_tick < 22:
            img = self.miss_img[self.miss_tick % 22 // 2]
        else:
            img = self.miss_img[11]

        if self.miss_tick > 40:
            self.miss_tick = 0
        return img

    def mellee_enemy_attack(self):
        self.tick += 1
        img = self.enemy_melee_attack_img[self.tick % self.enemy_melee_attack_time // 2]

        if self.tick == self.enemy_melee_attack_time:
            self.tick = 0

        return img

    def critical_enemy_attack(self):
        self.tick += 1
        img = self.enemy_critical_attack_img[self.tick % self.enemy_critical_attack_time // 2]

        if self.tick == self.enemy_critical_attack_time:
            self.tick = 0

        return img
