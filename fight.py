from settings import *
import pygame
from random import randint

sizes = {'roy': {'sword': [{'width': 124,
                            'height': 102,
                            'w': 11,
                            'h': 8,
                            'frames': 82,
                            'x': 230,
                            'y': 70,
                            'x1': 420,
                            'size': (550, 450),
                            'dmg_time': 70},

                           {'width': 142,
                            'height': 102,
                            'w': 12,
                            'h': 8,
                            'frames': 96,
                            'x': 130,
                            'y': 70,
                            'x1': 410,
                            'size': (650, 450),
                            'dmg_time': 95}]},

         'lyn': {'sword': [{'width': 118,
                            'height': 119,
                            'w': 7,
                            'h': 6,
                            'frames': 37,
                            'x': 280,
                            'y': 55,
                            'x1': 390,
                            'size': (530, 530),
                            'dmg_time': 25},

                           {'width': 220,
                            'height': 144,
                            'w': 9,
                            'h': 13,
                            'frames': 115,
                            'x': 60,
                            'y': 90,
                            'x1': 160,
                            'size': (970, 650),
                            'dmg_time': 75}],

                 'bow': [{'width': 136,
                          'height': 52,
                          'w': 3,
                          'h': 5,
                          'frames': 15,
                          'x': 400,
                          'y': 285,
                          'x1': 190,
                          'size': (610, 235),
                          'dmg_time': 25},

                         {'width': 143,
                          'height': 52,
                          'w': 3,
                          'h': 9,
                          'frames': 26,
                          'x': 365,
                          'y': 285,
                          'x1': 185,
                          'size': (650, 235),
                          'dmg_time': 50}]},

         'hector': {'axe': [{'width': 117,
                             'height': 99,
                             'w': 7,
                             'h': 6,
                             'frames': 33,
                             'x': 240,
                             'y': 110,
                             'x1': 430,
                             'size': (530, 450),
                             'dmg_time': 40},

                            {'width': 118,
                             'height': 99,
                             'w': 7,
                             'h': 6,
                             'frames': 32,
                             'x': 230,
                             'y': 110,
                             'x1': 435,
                             'size': (530, 450),
                             'dmg_time': 40}]},

         'eirika': {'lance': [{'width': 114,
                               'height': 67,
                               'w': 6,
                               'h': 5,
                               'frames': 28,
                               'x': 240,
                               'y': 220,
                               'x1': 450,
                               'size': (515, 300),
                               'dmg_time': 25},

                              {'width': 116,
                               'height': 70,
                               'w': 6,
                               'h': 6,
                               'frames': 32,
                               'x': 240,
                               'y': 225,
                               'x1': 450,
                               'size': (515, 300),
                               'dmg_time': 30}]},

         'ephraim': {'lance': [{'width': 114,
                                'height': 68,
                                'w': 6,
                                'h': 6,
                                'frames': 31,
                                'x': 230,
                                'y': 220,
                                'x1': 455,
                                'size': (515, 300),
                                'dmg_time': 45},

                               {'width': 122,
                                'height': 80,
                                'w': 6,
                                'h': 5,
                                'frames': 30,
                                'x': 195,
                                'y': 170,
                                'x1': 460,
                                'size': (550, 350),
                                'dmg_time': 35}]},

         'eliwood': {'sword': [{'width': 144,
                                'height': 106,
                                'w': 7,
                                'h': 6,
                                'frames': 40,
                                'x': 220,
                                'y': 50,
                                'x1': 330,
                                'size': (650, 480),
                                'dmg_time': 40},

                               {'width': 205,
                                'height': 126,
                                'w': 8,
                                'h': 8,
                                'frames': 59,
                                'x': 95,
                                'y': 50,
                                'x1': 180,
                                'size': (920, 570),
                                'dmg_time': 80}],

                     'lance': [{'width': 143,
                                'height': 89,
                                'w': 6,
                                'h': 6,
                                'frames': 35,
                                'x': 240,
                                'y': 145,
                                'x1': 305,
                                'size': (650, 400),
                                'dmg_time': 35},

                               {'width': 153,
                                'height': 82,
                                'w': 7,
                                'h': 6,
                                'frames': 40,
                                'x': 190,
                                'y': 185,
                                'x1': 340,
                                'size': (685, 360),
                                'dmg_time': 40}]
                     },

         'marth': {'sword': [{'width': 96,
                              'height': 67,
                              'w': 8,
                              'h': 4,
                              'frames': 29,
                              'x': 345,
                              'y': 270,
                              'x1': 425,
                              'size': (430, 300),
                              'dmg_time': 20},

                             {'width': 114,
                              'height': 101,
                              'w': 9,
                              'h': 8,
                              'frames': 70,
                              'x': 250,
                              'y': 80,
                              'x1': 435,
                              'size': (515, 450),
                              'dmg_time': 75}]},

         'ike': {'sword': [{'width': 96,
                            'height': 70,
                            'w': 5,
                            'h': 5,
                            'frames': 23,
                            'x': 330,
                            'y': 210,
                            'x1': 440,
                            'size': (430, 315),
                            'dmg_time': 30},

                           {'width': 150,
                            'height': 125,
                            'w': 7,
                            'h': 7,
                            'frames': 44,
                            'x': 300,
                            'y': -25,
                            'x1': 240,
                            'size': (675, 560),
                            'dmg_time': 40}]},

         'hero': {'sword': [{'width': 111,
                             'height': 108,
                             'w': 8,
                             'h': 7,
                             'frames': 55,
                             'x': 285,
                             'y': 60,
                             'x1': 415,
                             'size': (500, 485),
                             'dmg_time': 30},

                            {'width': 118,
                             'height': 109,
                             'w': 14,
                             'h': 14,
                             'frames': 186,
                             'x': 250,
                             'y': 50,
                             'x1': 410,
                             'size': (530, 490),
                             'dmg_time': 130}]},

         'sorcerer': {'magic': [{'width': 68,
                                 'height': 51,
                                 'w': 8,
                                 'h': 2,
                                 'frames': 16,
                                 'x': 255,
                                 'y': 295,
                                 'x1': 645,
                                 'size': (300, 225),
                                 'dmg_time': 25},

                                {'width': 80,
                                 'height': 111,
                                 'w': 8,
                                 'h': 8,
                                 'frames': 61,
                                 'x': 220,
                                 'y': 60,
                                 'x1': 620,
                                 'size': (360, 500),
                                 'dmg_time': 105}]},
         }

magic = {
    '1': {
        'width': 65,
        'height': 99,
        'w': 5,
        'h': 7,
        'frames': 35,
        'x': 600,
        'y': 90,
        'x1': 250},
    '2': {
        'width': 240,
        'height': 128,
        'w': 6,
        'h': 10,
        'frames': 56,
        'x': 0,
        'y': 0,
        'x1': 0}
}

magic_names = ['sorcerer']
weapon_img = {
    'iron_sword': pygame.transform.scale(pygame.image.load('templates/weapon/weapon.png').subsurface((16, 0, 16, 16)),
                                         (72, 72)),
    'iron_axe': pygame.transform.scale(pygame.image.load('templates/weapon/weapon.png').subsurface((119, 51, 16, 16)),
                                       (72, 72)),
    'iron_lance': pygame.transform.scale(pygame.image.load('templates/weapon/weapon.png').subsurface((34, 34, 16, 16)),
                                         (72, 72)),
    'bow': pygame.transform.scale(pygame.image.load('templates/weapon/weapon.png').subsurface((51, 85, 16, 16)),
                                  (72, 72)),
    'fire': pygame.transform.scale(pygame.image.load('templates/weapon/weapon.png').subsurface((51, 102, 16, 16)),
                                   (72, 72))}


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
    elif weapon_2 == 'bow' and weapon_1 is not 'magic':
        return True


class Fight_images:
    def __init__(self):
        self.images = {}
        self.magic_effects = {}

    def uppload_images(self, names):
        for name in names:
            if name not in self.images:
                # magic
                if name in magic_names:
                    self.magic_effects[name] = {'person': {'norm': [], 'crt': []}, 'enemy': {'norm': [], 'crt': []}}
                    # enemy magic
                    self.magic_effects[name]['enemy'] = {'norm': [pygame.transform.scale(
                        pygame.image.load(f'templates/persons/{name}/normal_effect.png').
                        subsurface(x * magic['1']['width'], y * magic['1']['height'],
                                   magic['1']['width'], magic['1']['height']), (290, 450))
                                                                     for y in range(magic['1']['h'])
                                                                     for x in range(magic['1']['w'])][
                                                                 :magic['1']['frames']],

                                                         'crt': [pygame.transform.scale(
                                                             pygame.image.load(
                                                                 f'templates/persons/{name}/critical_effect.png').
                                                             subsurface(x * magic['2']['width'],
                                                                        y * magic['2']['height'],
                                                                        magic['2']['width'], magic['2']['height']),
                                                             (WIDTH, HEIGHT)) for y in range(magic['2']['h'])
                                                                    for x in range(magic['2']['w'])][
                                                                :magic['2']['frames']]}
                    # person magic
                    self.magic_effects[name]['person']['norm'] = [pygame.transform.flip(i, True, False)
                                                                  for i in self.magic_effects[name]['enemy']['norm']]
                    self.magic_effects[name]['person']['crt'] = [pygame.transform.flip(i, True, False)
                                                                 for i in self.magic_effects[name]['enemy']['crt']]

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
        print(fight_images.images)
        self.person_hit = person.hit + (15 if triangle(person.type, enemy.type) else -15) - enemy.avoid
        self.enemy_hit = enemy.hit + (15 if triangle(enemy.type, person.type) else -15) - person.avoid
        self.moves = [True if randint(0, 100) <= person.crt else False,
                      True if randint(0, 100) <= (100 - self.person_hit) else False,
                      True if randint(0, 100) <= enemy.crt else False,
                      True if randint(0, 100) <= (100 - self.enemy_hit) else False]
        print(self.moves)
        # self.moves = [False, False, True, False]

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
        self.weapon_arrow = {'up': [pygame.transform.scale(pygame.image.load('templates/fight/up_arrow.png').
                                                           subsurface(x * 7, 0, 7, 10), (32, 45)) for x in range(3)],
                             'down': [pygame.transform.scale(pygame.image.load('templates/fight/down_arrow.png').
                                                             subsurface(x * 7, 0, 7, 10), (32, 45)) for x in range(3)]}
        self.person_weapon_arrow = self.weapon_arrow['up' if triangle(person.type, enemy.type) else 'down']
        self.enemy_weapon_arrow = self.weapon_arrow['up' if triangle(enemy.type, person.type) else 'down']

        # magic
        self.magic_img_id = -1
        self.person_magic_cords = (magic['2' if self.moves[0] else '1']['x'],
                                   magic['2' if self.moves[0] else '1']['y'])
        self.person_magic_cords_sms = (magic['2' if self.moves[0] else '1']['x1'],
                                       magic['2' if self.moves[0] else '1']['y'])
        self.enemy_magic_cords = (magic['2' if self.moves[2] else '1']['x1'],
                                  magic['2' if self.moves[2] else '1']['y'])
        self.enemy_magic_cords_sms = (magic['2' if self.moves[2] else '1']['x'],
                                      magic['2' if self.moves[2] else '1']['y'])
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

        # magic
        self.person_norm_effect = []
        self.person_critical_effect = []
        self.enemy_norm_effect = []
        self.enemy_critical_effect = []
        if person.name in fight_images.magic_effects:
            self.person_norm_effect = fight_images.magic_effects[person.name]['person']['norm']
            self.person_critical_effect = fight_images.magic_effects[person.name]['person']['crt']
            self.person_norm_effect_time = len(self.person_norm_effect) * 2
            self.person_critical_effect_time = len(self.person_critical_effect) * 2
        if enemy.name in fight_images.magic_effects:
            self.enemy_norm_effect = fight_images.magic_effects[enemy.name]['enemy']['norm']
            self.enemy_critical_effect = fight_images.magic_effects[enemy.name]['enemy']['crt']
            self.enemy_norm_effect_time = len(self.enemy_norm_effect) * 2
            self.enemy_critical_effect_time = len(self.enemy_critical_effect) * 2
        self.all_effects = self.person_norm_effect + self.person_critical_effect + \
                           self.enemy_norm_effect + self.enemy_critical_effect

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
