from settings import *
import pygame
from random import randint

sizes = {'roy': [{'width': 124,
                  'height': 102,
                  'w': 11,
                  'h': 8,
                  'frames': 82,
                  'x': 205,
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
                  'dmg_time': 95}],

         'lyn': [{'width': 118,
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

         'hector': [{'width': 117,
                     'height': 99,
                     'w': 7,
                     'h': 6,
                     'frames': 33,
                     'x': 230,
                     'y': 110,
                     'x1': 455,
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
                     'dmg_time': 40}],

         'eirika': [{'width': 114,
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
                     'dmg_time': 30}],

         'eliwood': [{'width': 144,
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

         'marth': [{'width': 96,
                    'height': 67,
                    'w': 8,
                    'h': 4,
                    'frames': 29,
                    'x': 325,
                    'y': 270,
                    'x1': 440,
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
                    'dmg_time': 75}],

         'ike': [{'width': 96,
                  'height': 70,
                  'w': 5,
                  'h': 5,
                  'frames': 23,
                  'x': 320,
                  'y': 220,
                  'x1': 450,
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
                  'dmg_time': 40}],

         'sorcerer': [{'width': 68,
                       'height': 51,
                       'w': 8,
                       'h': 2,
                       'frames': 16,
                       'x': 240,
                       'y': 300,
                       'x1': 665,
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
                       'dmg_time': 105}],
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
                    # magic
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
                self.images[name] = {'person': {'norm': [], 'crt': []}, 'enemy': {'norm': [], 'crt': []}}
                # enemy
                enemy_melee_attack_img = [pygame.image.load(f'templates/persons/{name}/normal_attack.png').
                                          subsurface(sizes[name][0]['width'] * x, sizes[name][0]['height'] * y,
                                                     sizes[name][0]['width'], sizes[name][0]['height'])
                                          for y in range(0, sizes[name][0]['h'])
                                          for x in range(0, sizes[name][0]['w'])][:sizes[name][0]['frames']]
                for i in range(len(enemy_melee_attack_img)):
                    enemy_melee_attack_img[i] = pygame.transform.scale(enemy_melee_attack_img[i],
                                                                       sizes[name][0]['size'])

                enemy_critical_attack_img = [pygame.image.load(f'templates/persons/{name}/critical_attack.png').
                                             subsurface(sizes[name][1]['width'] * x, sizes[name][1]['height'] * y,
                                                        sizes[name][1]['width'], sizes[name][1]['height'])
                                             for y in range(0, sizes[name][1]['h'])
                                             for x in range(0, sizes[name][1]['w'])][:sizes[name][1]['frames']]
                for i in range(len(enemy_critical_attack_img)):
                    enemy_critical_attack_img[i] = pygame.transform.scale(enemy_critical_attack_img[i],
                                                                          sizes[name][1]['size'])

                # person
                person_melee_attack_img = [pygame.transform.flip(img, True, False) for img in enemy_melee_attack_img]
                person_critical_attack_img = [pygame.transform.flip(img, True, False) for img in
                                              enemy_critical_attack_img]

                self.images[name]['person']['norm'] = person_melee_attack_img
                self.images[name]['person']['crt'] = person_critical_attack_img
                self.images[name]['enemy']['norm'] = enemy_melee_attack_img
                self.images[name]['enemy']['crt'] = enemy_critical_attack_img


class Fight:
    def __init__(self, person, enemy, fight_images, person_dmg=0, enemy_dmg=0):
        self.moves = [True if randint(0, 100) <= person.crt else False,
                      True if randint(0, 100) <= (1 - person.hit) else False,
                      True if randint(0, 100) <= enemy.crt else False,
                      True if randint(0, 100) <= (1 - enemy.hit) else False]
        print(self.moves)

        self.without_enemy_attack = False
        self.person_double_attack = False
        self.enemy_double_attack = False
        if abs(person.pos[0] - enemy.pos[0]) + abs(person.pos[1] - enemy.pos[1]) <= person.range_attack:
            if abs(person.pos[0] - enemy.pos[0]) + abs(person.pos[1] - enemy.pos[1]) > enemy.range_attack:
                self.without_enemy_attack = True
                print('without')
        if person.attack_speed - enemy.attack_speed >= 4:
            self.person_double_attack = True
            self.moves.append(True if randint(0, 100) <= (1 - person.hit) else False)
            print('person double attack')
        elif enemy.attack_speed - person.attack_speed >= 4:
            self.enemy_double_attack = True
            self.moves.append(True if randint(0, 100) <= enemy.crt else False)
            self.moves.append(True if randint(0, 100) <= (1 - enemy.hit) else False)
            print('enemy double attack')

        self.need_moves = [0, 0]
        self.tick = 0
        self.dodge_tick = 0
        self.miss_tick = 0
        self.magic_tick = 0
        self.enemy_dead = 0
        self.person_dead = 0

        self.person_x, self.person_y = sizes[person.name][int(self.moves[0])]['x'], \
                                       sizes[person.name][int(self.moves[0])]['y']
        self.enemy_x, self.enemy_y = sizes[enemy.name][int(self.moves[2])]['x1'], \
                                     sizes[enemy.name][int(self.moves[2])]['y']
        self.person_dmg_tick = sizes[enemy.name][int(self.moves[2])]['dmg_time']
        self.enemy_dmg_tick = sizes[person.name][int(self.moves[0])]['dmg_time']
        self.person_dmg = person_dmg
        self.enemy_dmg = enemy_dmg
        self.person_img_id = 0
        self.enemy_img_id = 0

        self.magic_img_id = -1
        self.person_magic_cords = (magic['2' if self.moves[0] else '1']['x'],
                                   magic['2' if self.moves[0] else '1']['y'])
        self.person_magic_cords_sms = (magic['2' if self.moves[0] else '1']['x1'],
                                       magic['2' if self.moves[0] else '1']['y'])
        self.enemy_magic_cords = (magic['2' if self.moves[2] else '1']['x1'],
                                  magic['2' if self.moves[2] else '1']['y'])
        self.enemy_magic_cords_sms = (magic['2' if self.moves[2] else '1']['x'],
                                      magic['2' if self.moves[2] else '1']['y'])

        self.fight_bg = pygame.image.load('templates/fight/bg.png').subsurface(1, 1, 240, 160)
        self.fight_bg = pygame.transform.scale(self.fight_bg, (WIDTH, HEIGHT))
        self.fight_characters = pygame.image.load('templates/fight/baze.png')
        self.fight_characters = pygame.transform.scale(self.fight_characters, (WIDTH, HEIGHT))
        self.numbers = [pygame.transform.scale(
            pygame.image.load('templates/fight/numbers.png').subsurface(i * 8, 0, 8, 8), (40, 40)) for i in range(10)]
        self.hp = [pygame.transform.scale(
            pygame.image.load('templates/fight/hp.png').subsurface(i * 2, 0, 2, 7), (10, 35)) for i in range(2)]

        self.miss_img = [pygame.image.load(f'templates/miss/{i}.png') for i in range(0, 12)]
        for i in range(len(self.miss_img)):
            self.miss_img[i] = pygame.transform.scale(self.miss_img[i], (100, 100))

        # persons
        self.person_melee_attack_img = fight_images.images[person.name]['person']['norm']
        self.person_critical_attack_img = fight_images.images[person.name]['person']['crt']
        self.all_person_img = self.person_melee_attack_img + self.person_critical_attack_img
        self.enemy_melee_attack_img = fight_images.images[enemy.name]['enemy']['norm']
        self.enemy_critical_attack_img = fight_images.images[enemy.name]['enemy']['crt']
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
        if self.miss_tick < 66:
            img = self.miss_img[self.miss_tick % 66 // 6]
        else:
            img = self.miss_img[11]

        if self.miss_tick > 120:
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
