from settings import *
import pygame
from random import randint
from data.weapon import weapon, weapon_img, weapon_arrow, weapon_effective, weapon_have_triangle_bonus
from data.classes import types
from data.persons import characters
from person import lords

magic_names = ['sophia', 'lina']

magic = {'fire': {'width': 240,
                  'height': 160,
                  'w': 4,
                  'h': 3,
                  'frames': 12,
                  'x': 0,
                  'y': 50,
                  'x1': 150,
                  'size': (1080, 720),
                  'delay': 30},

         'elfire': {'width': 240,
                    'height': 160,
                    'w': 4,
                    'h': 4,
                    'frames': 16,
                    'x': 100,
                    'y': 50,
                    'x1': 50,
                    'size': (1080, 720),
                    'delay': 25},

         'fimbulvetr': {'width': 240,
                        'height': 160,
                        'w': 4,
                        'h': 11,
                        'frames': 43,
                        'x': 100,
                        'y': 50,
                        'x1': 50,
                        'size': (1080, 720),
                        'delay': 0},

         'excalibur': {'width': 245,
                       'height': 160,
                       'w': 5,
                       'h': 4,
                       'frames': 43,
                       'x': 0,
                       'y': 0,
                       'x1': 0,
                       'size': (1200, 800),
                       'delay': 0},

         'miracle': {'width': 160,
                     'height': 126,
                     'w': 5,
                     'h': 3,
                     'frames': 15,
                     'x': 400,
                     'y': 0,
                     'x1': 0,
                     'size': (720, 570),
                     'delay': 25},

         'divine': {'width': 241,
                    'height': 161,
                    'w': 5,
                    'h': 4,
                    'frames': 43,
                    'x': 100,
                    'y': 50,
                    'x1': 50,
                    'size': (1080, 720),
                    'delay': 10},

         'lightning': {'width': 241,
                       'height': 161,
                       'w': 5,
                       'h': 7,
                       'frames': 32,
                       'x': 100,
                       'y': 50,
                       'x1': 50,
                       'size': (1080, 720),
                       'delay': 0},

         'flux': {'width': 65,
                  'height': 99,
                  'w': 5,
                  'h': 7,
                  'frames': 35,
                  'x': 600,
                  'y': 85,
                  'x1': 260,
                  'size': (290, 450),
                  'delay': 0},

         'ereshkigal': {'width': 240,
                        'height': 128,
                        'w': 6,
                        'h': 10,
                        'frames': 56,
                        'x': 0,
                        'y': 0,
                        'x1': 0,
                        'size': (1200, 800),
                        'delay': 0},
         }


def types_class(class_):
    for type_ in types:
        if class_ in types[type_]:
            return type_
    return None


def triangle(weapon_1, weapon_2):
    if weapon_1 in weapon_have_triangle_bonus:
        return True
    else:
        if weapon_1 == weapon_2:
            return None
        if weapon[weapon_1]['class'] == 'magic' and weapon[weapon_2]['class'] == 'magic':
            weapon_1 = weapon[weapon_1]['subclass']
            weapon_2 = weapon[weapon_2]['subclass']
            if weapon_1 == 'dark':
                if weapon_2 == 'anima':
                    return True
                elif weapon_2 == 'light':
                    return False
            elif weapon_1 == 'anima':
                if weapon_2 == 'light':
                    return True
                elif weapon_2 == 'dark':
                    return False
            elif weapon_1 == 'light':
                if weapon_2 == 'dark':
                    return True
                elif weapon_2 == 'anima':
                    return False
        else:
            weapon_1 = weapon[weapon_1]['class']
            weapon_2 = weapon[weapon_2]['class']
            if weapon_1 == 'sword':
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
    return None


def calculate_damage(person, enemy):
    if person.weapon in weapon_have_triangle_bonus:
        bonus = 2
    else:
        if triangle(person.weapon.name, enemy.weapon.name) is None:
            bonus = 0
        elif triangle(person.weapon.name, enemy.weapon.name):
            bonus = 1
        else:
            bonus = -1

        if person.weapon.class_ != 'magic' or enemy.weapon.class_ != 'magic':
            if person.weapon.class_ == enemy.weapon.class_:
                bonus = 0
        else:
            if weapon[person.weapon.name]['subclass'] == weapon[enemy.weapon.name]['subclass']:
                bonus = 0

    effective = 1
    if types_class(enemy.class_) is None:
        pass
    elif person.weapon.name in weapon_effective[types_class(enemy.class_)]:
        effective = 2
    dmg = (person.dmg + bonus) * effective
    def_ = enemy.res if person.weapon.class_ == 'magic' else enemy.def_
    return dmg - def_


class Fight_images:
    def __init__(self):
        self.images = {}
        self.magic_effects = {}
        self.uploaded_images = False

    def read(self, file, weapon_='', script=False):
        if script:
            result = {'attack': [], 'critical': []}
            dmg_times = {'attack': 0, 'critical': 0}
            for attack in result:
                res = []
                dmg_time = 0
                dmg_end = False
                for i in file:
                    if i[:2] == 'f;':
                        if not dmg_end:
                            dmg_time += int(i[2:3])
                        res.append(i[:-1].split(';'))
                    elif i[:12] == 'wait_for_hit':
                        dmg_end = True
                    elif i[:4] == 'pose' and len(res) > 1:
                        break
                result[attack] = [[int(i[2].split('_')[1]), int(i[1])] for i in res]
                dmg_times[attack] = dmg_time

            return result, dmg_times
        else:
            res = [[i[:-1].split(';')[0]] + i[:-1].split(';')[1].split(',') +
                   i[:-1].split(';')[2].split(',') + i[:-1].split(';')[3].split(',')
                   for i in file]
            result = []
            for i in res:
                if i[0][len(weapon_) + 5:len(weapon_) + 10] == 'under':
                    result[len(result) - 1].append([int(j) for j in i[1:]])
                else:
                    result.append([[int(j) for j in i[1:]]])
            return result

    def upload_images(self, names):
        for person in names:
            h_ = person.split('/')
            name = h_[0]
            class_ = h_[1]
            if name not in self.images:
                if name in magic_names and not self.uploaded_images:
                    self.uploaded_images = True
                    # magic
                    for magic_ in magic:
                        self.magic_effects[magic_] = {'person': [], 'enemy': []}
                        # enemy magic
                        self.magic_effects[magic_]['enemy'] = [pygame.transform.scale(
                            pygame.image.load(f'templates/magic/{magic_}.png').convert_alpha().
                            subsurface(x * magic[f'{magic_}']['width'], y * magic[f'{magic_}']['height'],
                                       magic[f'{magic_}']['width'], magic[f'{magic_}']['height']),
                            magic[f'{magic_}']['size'])
                                                                  for y in range(magic[f'{magic_}']['h'])
                                                                  for x in range(magic[f'{magic_}']['w'])][
                                                              :magic[f'{magic_}']['frames']]

                        # person magic
                        self.magic_effects[magic_]['person'] = [pygame.transform.flip(i, True, False)
                                                                for i in self.magic_effects[magic_]['enemy']]

                # persons
                if name in lords:
                    w_ = characters[name]['can_use']
                    t_ = 1 if class_ == characters[name]['class'] else 2
                    self.images[person] = {i: [] for i in w_}
                    for weapon_ in w_:
                        self.images[person][weapon_] = {'person': [], 'enemy': []}
                        index = self.read(open(f'templates/persons/lords/{name}/battle/T{t_}/{weapon_}/Index.txt').readlines(), weapon_)
                        enemy_attack_img = []
                        image = pygame.image.load(f'templates/persons/lords/{name}/battle/T{t_}/{weapon_}/attack.png').convert_alpha()
                        for j in index:
                            ar_ = []
                            for i in j:
                                img = pygame.transform.scale(image.subsurface((i[0], i[1], i[2], i[3])), (i[2] * 5, i[3] * 5))
                                ar_.append(img)
                            enemy_attack_img.append(ar_)
                        # person
                        person_attack_img = [[pygame.transform.flip(img, True, False) for img in array] for array in enemy_attack_img]

                        self.images[person][weapon_]['person'] = person_attack_img
                        self.images[person][weapon_]['enemy'] = enemy_attack_img
                else:
                    try:
                        w_ = characters[name]['can_use' if class_ == characters[name]['class'] else 't2_can_use']
                        self.images[person] = {i: [] for i in w_}
                        for weapon_ in w_:
                            self.images[person][weapon_] = {'person': [], 'enemy': []}
                            index = self.read(open(f'templates/persons/other/{class_}/{name}/battle/{weapon_}/Index.txt').readlines(), weapon_)
                            enemy_attack_img = []
                            image = pygame.image.load(f'templates/persons/other/{class_}/{name}/battle/{weapon_}/attack.png').convert_alpha()
                            for j in index:
                                ar_ = []
                                for i in j:
                                    img = pygame.transform.scale(image.subsurface((i[0], i[1], i[2], i[3])), (i[2] * 5, i[3] * 5))
                                    ar_.append(img)
                                enemy_attack_img.append(ar_)
                            # person
                            person_attack_img = [[pygame.transform.flip(img, True, False) for img in array] for array in enemy_attack_img]

                            self.images[person][weapon_]['person'] = person_attack_img
                            self.images[person][weapon_]['enemy'] = enemy_attack_img
                    except:
                        w_ = characters[name]['can_use' if class_ == characters[name]['class'] else 't2_can_use']
                        g_ = characters[name]['gender']
                        self.images[person] = {i: [] for i in w_}
                        for weapon_ in w_:
                            self.images[person][weapon_] = {'person': [], 'enemy': []}
                            index = self.read(
                                open(f'templates/persons/other/{class_}/{g_}/battle/{weapon_}/Index.txt').readlines(),
                                weapon_)
                            enemy_attack_img = []
                            image = pygame.image.load(
                                f'templates/persons/other/{class_}/{g_}/battle/{weapon_}/attack.png').convert_alpha()
                            for j in index:
                                ar_ = []
                                for i in j:
                                    img = pygame.transform.scale(image.subsurface((i[0], i[1], i[2], i[3])),
                                                                 (i[2] * 5, i[3] * 5))
                                    ar_.append(img)
                                enemy_attack_img.append(ar_)
                            # person
                            person_attack_img = [[pygame.transform.flip(img, True, False) for img in array] for array in
                                                 enemy_attack_img]

                            self.images[person][weapon_]['person'] = person_attack_img
                            self.images[person][weapon_]['enemy'] = enemy_attack_img


class Fight:
    def __init__(self, person, enemy, fight_images, not_my_fight=False):
        self.fight_img = fight_images
        print(self.fight_img.images)
        self.img = None
        self.person = person
        self.enemy = enemy
        self.tick = 0

        self.person_dmg = calculate_damage(person, enemy)
        self.enemy_dmg = calculate_damage(enemy, person)
        if self.person_dmg < 0:
            self.person_dmg = 0
        if self.enemy_dmg < 0:
            self.enemy_dmg = 0

        self.person_hit = person.hit - enemy.avoid
        self.enemy_hit = enemy.hit - person.avoid
        if triangle(person.weapon.name, enemy.weapon.name) is None:
            pass
        elif triangle(person.weapon.name, enemy.weapon.name):
            self.person_hit += 15
            self.enemy_hit -= 15
        else:
            self.person_hit -= 15
            self.enemy_hit += 15

        self.moves = [False,
                      True if randint(0, 100) <= (100 - self.person_hit) else False,
                      False,
                      True if randint(0, 100) <= (100 - self.enemy_hit) else False]
        # self.moves = [False, False, False, False]

        self.person_count_attack = 1
        self.enemy_count_attack = 1
        self.distance_fight = False
        range_persons = abs(person.pos[0] - enemy.pos[0]) + abs(person.pos[1] - enemy.pos[1])
        if person.attack_speed - enemy.attack_speed >= 4:
            self.person_count_attack = 2
        elif enemy.attack_speed - person.attack_speed >= 4:
            self.enemy_count_attack = 2
        if range_persons not in enemy.weapon.range:
            self.enemy_count_attack = 0

        if person.weapon.name in ['brave_sword', 'brave_axe', 'brave_lance', 'brave_bow']:
            self.person_count_attack = self.person_count_attack * 2
        if enemy.weapon.name in ['brave_sword', 'brave_axe', 'brave_lance', 'brave_bow']:
            self.enemy_count_attack = self.enemy_count_attack * 2

        if range_persons > 1:
            self.distance_fight = True

        self.need_moves = [0, 0]
        self.attack_tick = 0
        self.cadr = 0
        self.dodge_tick = 0
        self.miss_tick = 0
        self.magic_tick = 0

        # weapon
        self.person_weapon_img = weapon_img[person.weapon.name]
        self.enemy_weapon_img = weapon_img[enemy.weapon.name]

        self.person_img_id = 0
        self.enemy_img_id = 0
        self.person_weapon_arrow = weapon_arrow['up' if triangle(person.weapon.name, enemy.weapon.name) else 'down']
        self.enemy_weapon_arrow = weapon_arrow['up' if triangle(enemy.weapon.name, person.weapon.name) else 'down']

        # magic
        self.magic_img_id = -1
        self.person_magic_cords = (1, 1)
        self.person_magic_cords_sms = (1, 1)
        self.enemy_magic_cords = (1, 1)
        self.enemy_magic_cords_sms = (1, 1)
        self.person_magic_effect = []
        self.enemy_magic_effect = []
        self.person_magic_effect_time = 0
        self.enemy_magic_effect_time = 0

        if person.weapon.class_ == 'magic':
            self.person_magic_cords = (magic[person.weapon.name]['x'], magic[person.weapon.name]['y'])
            self.person_magic_cords_sms = (magic[person.weapon.name]['x1'], magic[person.weapon.name]['y'])

            self.person_magic_effect = self.fight_img.magic_effects[person.weapon.name]['person']
            self.person_magic_effect_time = len(self.person_magic_effect) * 2
            self.person_magic_delay = magic[person.weapon.name]['delay']

        if enemy.weapon.class_ == 'magic':
            self.enemy_magic_cords = (magic[enemy.weapon.name]['x1'], magic[enemy.weapon.name]['y'])
            self.enemy_magic_cords_sms = (magic[enemy.weapon.name]['x'], magic[enemy.weapon.name]['y'])

            self.enemy_magic_effect = self.fight_img.magic_effects[enemy.weapon.name]['enemy']
            self.enemy_magic_effect_time = len(self.enemy_magic_effect) * 2
            self.enemy_magic_delay = magic[enemy.weapon.name]['delay']

        if not_my_fight:
            self.all_effects = self.enemy_magic_effect + self.person_magic_effect
        else:
            self.all_effects = self.person_magic_effect + self.enemy_magic_effect

        if self.distance_fight:
            if self.person_magic_cords != (0, 0):
                self.person_magic_cords = (self.person_magic_cords[0] + 200, self.person_magic_cords[1])
                self.person_magic_cords_sms = (self.person_magic_cords_sms[0] - 200, self.person_magic_cords_sms[1])
            if self.enemy_magic_cords != (0, 0):
                self.enemy_magic_cords = (self.enemy_magic_cords[0] - 200, self.enemy_magic_cords[1])
                self.enemy_magic_cords_sms = (self.enemy_magic_cords_sms[0] + 200, self.enemy_magic_cords_sms[1])

        # base
        self.fight_bg = pygame.image.load('templates/fight/bg.png').subsurface(2, 2, 240, 160)
        if self.distance_fight:
            self.fight_characters = pygame.image.load('templates/fight/distance_baze.png')
        else:
            self.fight_characters = pygame.image.load('templates/fight/baze.png')
        self.fight_bg = pygame.transform.scale(self.fight_bg, (1200, 800))
        self.fight_characters = pygame.transform.scale(self.fight_characters, (1200, 800))
        self.numbers = [pygame.transform.scale(
            pygame.image.load('templates/numbers/numbers.png').subsurface(i * 8, 0, 8, 8), (40, 40)) for i in range(10)]
        self.hp = [pygame.transform.scale(
            pygame.image.load('templates/fight/hp.png').subsurface(i * 2, 0, 2, 7), (10, 35)) for i in range(2)]

        self.miss_img = [pygame.image.load(f'templates/miss/{i}.png') for i in range(0, 12)]
        for i in range(len(self.miss_img)):
            self.miss_img[i] = pygame.transform.scale(self.miss_img[i], (100, 100))

        # persons
        person_weapon_class = person.weapon.class_
        # if self.distance_fight:
        #     if range_persons in person.weapon.range:
        #         if person_weapon_class == 'axe' and 'distance_axe' in self.fight_img.images[person.name]:
        #             person_weapon_class = 'distance_axe'
        #         elif person_weapon_class == 'lance' and 'distance_lance' in self.fight_img.images[person.name]:
        #             person_weapon_class = 'distance_lance'
        enemy_weapon_class = enemy.weapon.class_
        # if self.distance_fight:
        #     if range_persons in enemy.weapon.range:
        #         if enemy_weapon_class == 'axe' and 'distance_axe' in self.fight_img.images[enemy.name]:
        #             enemy_weapon_class = 'distance_axe'
        #         elif enemy_weapon_class == 'lance' and 'distance_lance' in self.fight_img.images[enemy.name]:
        #             enemy_weapon_class = 'distance_lance'

        # files
        self.person_attack_img = self.fight_img.images[person.name + '/' + person.class_][person_weapon_class]['person']
        if person.name in lords:
            t_ = 'T1' if self.person.lvl < 10 else 'T2'
            self.person_index = self.fight_img.read(open(f'templates/persons/lords/{self.person.name}/battle/{t_}/'
                                                         f'{self.person.weapon.class_}/Index.txt'), person.weapon.class_)
            self.person_script, self.person_times = self.fight_img.read(open(f'templates/persons/lords/{self.person.name}/battle/{t_}/'
                                                                        f'{self.person.weapon.class_}/Script.txt'), '', True)
        else:
            try:
                self.person_index = self.fight_img.read(open(f'templates/persons/other/{self.person.class_}/{person.name}/battle/'
                                                             f'{self.person.weapon.class_}/Index.txt'), person.weapon.class_)
                self.person_script, self.person_times = self.fight_img.read(open(f'templates/persons/other/{self.person.class_}/{person.name}/battle/'
                                                                                 f'{self.person.weapon.class_}/Script.txt'), '', True)
            except:
                self.person_index = self.fight_img.read(open(f'templates/persons/other/{self.person.class_}/{person.gender}/battle/'
                                                             f'{self.person.weapon.class_}/Index.txt'), person.weapon.class_)
                self.person_script, self.person_times = self.fight_img.read(open(f'templates/persons/other/{self.person.class_}/{person.gender}/battle/'
                                                                            f'{self.person.weapon.class_}/Script.txt'), '', True)
        self.person_stay_img = self.person_attack_img[0]

        self.enemy_attack_img = self.fight_img.images[enemy.name + '/' + enemy.class_][enemy_weapon_class]['enemy']
        if enemy.name in lords:
            t_ = 'T1' if self.enemy.lvl < 10 else 'T2'
            self.enemy_index = self.fight_img.read(open(f'templates/persons/lords/{self.enemy.name}/battle/{t_}/'
                                                        f'{self.enemy.weapon.class_}/Index.txt'), enemy.weapon.class_)
            self.enemy_script, self.enemy_times = self.fight_img.read(open(f'templates/persons/lords/{self.enemy.name}/battle/{t_}/'
                                                                      f'{self.enemy.weapon.class_}/Script.txt'), '', True)
        else:
            try:
                self.enemy_index = self.fight_img.read(open(f'templates/persons/other/{self.enemy.class_}/{enemy.name}/battle/'
                                                            f'{self.enemy.weapon.class_}/Index.txt'), enemy.weapon.class_)
                self.enemy_script, self.enemy_times = self.fight_img.read(open(f'templates/persons/other/{self.enemy.class_}/{enemy.name}/battle/'
                                                                          f'{self.enemy.weapon.class_}/Script.txt'), '', True)
            except:
                self.enemy_index = self.fight_img.read(open(f'templates/persons/other/{self.enemy.class_}/{enemy.gender}/battle/'
                                                            f'{self.enemy.weapon.class_}/Index.txt'), enemy.weapon.class_)
                self.enemy_script, self.enemy_times = self.fight_img.read(open(f'templates/persons/other/{self.enemy.class_}/{enemy.gender}/battle/'
                                                                               f'{self.enemy.weapon.class_}/Script.txt'), '', True)
        self.enemy_stay_img = self.enemy_attack_img[0]

        self.img = self.person_stay_img
        self.img_ = self.enemy_stay_img

        self.person_dmg_time = self.person_times['critical' if self.moves[0] else 'attack']
        self.enemy_dmg_time = self.enemy_times['critical' if self.moves[2] else 'attack']

        self.person_x, self.person_y = self.person_index[0][0][4] + 100, self.person_index[0][0][5] + 200
        self.enemy_x, self.enemy_y = self.enemy_index[0][0][4] + 100 + 300, self.enemy_index[0][0][5] + 200

        # attack time
        self.person_attack_time = sum([i[1] for i in self.person_script['critical' if self.moves[0] else 'attack']])
        self.enemy_attack_time = sum([i[1] for i in self.enemy_script['critical' if self.moves[2] else 'attack']])

        # time
        self.start_enemy_attack = 50 + self.person_attack_time + 100

        self.person_dmg_tick = 50 + self.person_dmg_time
        self.enemy_dmg_tick = self.start_enemy_attack + self.enemy_dmg_time

        if self.person.weapon.class_ == 'magic':
            self.end = self.start_enemy_attack + max(self.enemy_magic_effect_time, self.enemy_attack_time) + 50
        else:
            self.end = self.start_enemy_attack + self.enemy_attack_time + 50

        self.cadr = 0
        self.cadr_tick = 0
        self.script_navigator = 0

        self.dead_tick = 0
        self.death_opacity = [0, 20, 20, 20, 20, 44, 44, 44, 44, 64,
                              64, 64, 64, 84, 84, 84, 108, 108, 108, 108,
                              128, 128, 128, 128, 148, 148, 148, 148, 172, 172,
                              172, 192, 192, 192, 192, 212, 212, 212, 212, 236,
                              236, 236, 236, 255, 255, 255, 0, 0, 0, 0,
                              0, 0, -1, 0, 0, 0, 0, 0, 0, 255,
                              0, 0, 0, 0, 0, 0, 255, 0, 0, 0,
                              0, 0, 0, 255, 0, 0, 0, 0, 0, 0,
                              255, 0, 0, 0, 0, 0, 0]
        self.person_dead = False
        self.enemy_dead = False

        # fonts
        self.f1 = pygame.font.Font(None, 30)
        self.f2 = pygame.font.Font(None, 50)
        self.f3 = pygame.font.Font(None, 70)

    def attack(self, script, person=True):
        self.cadr_tick += 1
        if self.cadr_tick == script[self.script_navigator][1]:
            self.cadr = script[self.script_navigator][0]
            self.cadr_tick = 0
            self.script_navigator += 1
            if self.script_navigator == len(script):
                self.script_navigator = 0
                self.cadr = 0
                self.cadr_tick = 0
        return self.person_attack_img[self.cadr] if person else self.enemy_attack_img[self.cadr]

    def miss(self):
        self.miss_tick += 1
        if self.miss_tick < 22:
            img = self.miss_img[self.miss_tick % 22 // 2]
        else:
            img = self.miss_img[11]

        if self.miss_tick > 40:
            self.miss_tick = 0
        return img

    def render_base_for_fight(self, screen):
        x_, y_ = 360, 240

        # bg
        screen.fill(BLACK)
        screen.blit(self.fight_bg, (x_, y_))
        screen.blit(self.fight_characters, (x_, y_))

        # characters person
        text_name = self.f3.render(self.person.name, True, WHITE)
        screen.blit(text_name, (50 + x_, 50 + y_))

        hit = str(self.person_hit) if self.person_hit > 0 else f'0{self.person_hit}'
        dmg = str(self.person_dmg) if self.person_dmg > 9 else f'0{self.person_dmg}'
        crt = str(self.person.crt) if self.person.crt > 9 else f'0{self.person.crt}'
        for i in range(len(hit)):
            if len(hit) < 3:
                screen.blit(self.numbers[int(hit[i])], (120 + i * 40 + x_, 560 + y_))
            else:
                screen.blit(self.numbers[int(hit[i])], (80 + i * 40 + x_, 560 + y_))
        for i in range(len(dmg)):
            screen.blit(self.numbers[int(dmg[i])], (120 + i * 40 + x_, 600 + y_))
        for i in range(len(crt)):
            screen.blit(self.numbers[int(crt[i])], (120 + i * 40 + x_, 640 + y_))

        # characters enemy
        text_name = self.f3.render(self.enemy.name, True, WHITE)
        screen.blit(text_name, (1000 + x_, 50 + y_))

        hit = str(self.enemy_hit) if self.enemy_hit > 0 else f'0{self.enemy_hit}'
        dmg = str(self.enemy_dmg) if self.enemy_dmg > 9 else f'0{self.enemy_dmg}'
        crt = str(self.enemy.crt) if self.enemy.crt > 9 else f'0{self.enemy.crt}'
        for i in range(len(hit)):
            if len(hit) < 3:
                screen.blit(self.numbers[int(hit[i])], (1115 + i * 40 + x_, 560 + y_))
            else:
                screen.blit(self.numbers[int(hit[i])], (1075 + i * 40 + x_, 560 + y_))
        for i in range(len(dmg)):
            screen.blit(self.numbers[int(dmg[i])], (1115 + i * 40 + x_, 600 + y_))
        for i in range(len(crt)):
            screen.blit(self.numbers[int(crt[i])], (1115 + i * 40 + x_, 640 + y_))

        # hp
        text_hp = str(self.person.hp) if self.person.hp > 0 else '0'
        for i in range(len(text_hp)):
            screen.blit(self.numbers[int(text_hp[i])], (20 + i * 40 + x_, 725 + y_))

        for i in range(2 if self.person.max_hp > 45 else 1):
            if self.person.max_hp > 45:
                for j in range(0, 45):
                    screen.blit(self.hp[0 if j + i * 45 < self.person.hp else 1],
                                (110 + j * 10 + x_, 705 + y_ if i == 0 else 745 + y_))
            else:
                for j in range(0, self.person.max_hp):
                    screen.blit(self.hp[0 if j < self.person.hp else 1],
                                (110 + j * 10 + x_, 726 + y_))

        text_hp = str(self.enemy.hp) if self.enemy.hp > 0 else '0'
        for i in range(len(text_hp)):
            screen.blit(self.numbers[int(text_hp[i])], (630 + i * 40 + x_, 725 + y_))
        for i in range(2 if self.enemy.max_hp > 45 else 1):
            if self.enemy.max_hp > 45:
                for j in range(0, 45):
                    screen.blit(self.hp[0 if j + i * 45 < self.enemy.hp else 1],
                                (720 + j * 10 + x_, 705 + y_ if i == 0 else 745 + y_))
            else:
                for j in range(0, self.enemy.max_hp):
                    screen.blit(self.hp[0 if j < self.enemy.hp else 1],
                                (720 + j * 10 + x_, 726 + y_))

        # weapon
        screen.blit(self.person_weapon_img, (220 + x_, 608 + y_))
        screen.blit(self.enemy_weapon_img, (620 + x_, 608 + y_))
        screen.blit(self.person_weapon_arrow[self.tick % 30 // 10 if self.tick % 60 < 30 else 0], (272 + x_, 635 + y_))
        screen.blit(self.enemy_weapon_arrow[self.tick % 30 // 10 if self.tick % 60 < 30 else 0], (672 + x_, 635 + y_))
        text1 = self.f2.render(self.person.weapon.name, True, BLACK)
        text2 = self.f2.render(self.enemy.weapon.name, True, BLACK)
        screen.blit(text1, (310 + x_, 625 + y_))
        screen.blit(text2, (710 + x_, 625 + y_))

        return x_, y_

    def render_fight(self, screen):
        self.tick += 1

        # deal damage
        for person in [self.person] + [self.enemy]:
            if person.damage_for_me > 0:
                person.hp -= 1
                person.damage_for_me -= 1

        if self.tick <= 50:
            pass
        else:
            # person
            if self.person.hp <= 0:
                if self.dead_tick < len(self.death_opacity) - 1:
                    for i in self.img:
                        i.set_alpha(self.death_opacity[self.dead_tick])
                self.dead_tick += 1
                if self.dead_tick == len(self.death_opacity) + 50:
                    return None
            elif self.tick <= 50 + self.person_attack_time and not self.enemy_dead:
                self.img = self.attack(self.person_script['critical' if self.moves[0] else 'attack'])
            else:
                self.img = self.person_stay_img

            # enemy
            if self.enemy.hp <= 0:
                if self.dead_tick < len(self.death_opacity) - 1:
                    for i in self.img_:
                        i.set_alpha(self.death_opacity[self.dead_tick])
                self.dead_tick += 1
                if self.dead_tick == len(self.death_opacity) + 50:
                    return None
            elif (self.tick >= self.start_enemy_attack) and \
                    (self.tick <= self.start_enemy_attack + self.enemy_attack_time) and not self.person_dead:
                self.img_ = self.attack(self.enemy_script['critical' if self.moves[2] else 'attack'], False)
            else:
                self.img_ = self.enemy_stay_img

            # damage
            if not self.moves[1]:
                if self.tick == self.person_dmg_tick + 5:
                    k_ = 3 if self.moves[0] else 1
                    self.enemy.damage_for_me = self.person_dmg * k_

            if not self.moves[3]:
                if self.tick == self.enemy_dmg_tick + 5:
                    k_ = 3 if self.moves[2] else 1
                    self.person.damage_for_me = self.enemy_dmg * k_

        # magic effect
        magic_img = None
        if self.person.weapon.name in self.fight_img.magic_effects:
            if (self.tick > 55 + self.person_magic_delay) and \
                    (self.tick <= 55 + self.person_magic_delay + self.person_magic_effect_time):
                self.magic_tick += 1
                magic_img = self.person_magic_effect[
                    self.magic_tick % self.person_magic_effect_time // 2]
                if self.tick == 55 + self.person_magic_delay + self.person_magic_effect_time:
                    self.magic_tick = 0
                    magic_img = None

        if self.enemy.weapon.name in self.fight_img.magic_effects:
            if (self.tick > self.start_enemy_attack + self.enemy_magic_delay) and \
                    (self.tick <= self.start_enemy_attack + self.enemy_magic_delay +
                     self.enemy_magic_effect_time):
                self.magic_tick += 1
                magic_img = self.enemy_magic_effect[
                    self.magic_tick % self.enemy_magic_effect_time // 2]
                if self.tick == self.start_enemy_attack + self.enemy_magic_delay + \
                        self.enemy_magic_effect_time:
                    self.magic_tick = 0
                    magic_img = None

        if self.tick < self.start_enemy_attack:
            cords_ = self.person_magic_cords_sms
        else:
            cords_ = self.enemy_magic_cords_sms

        # fight base
        x_, y_ = self.render_base_for_fight(screen)

        # persons
        for i in range(len(self.img)):
            if self.tick < self.start_enemy_attack:
                c_ = (1550 - self.person_index[self.cadr][i][2] * 5 - self.person_index[self.cadr][i][4] * 5 -
                      (200 if self.distance_fight else 0), self.person_index[self.cadr][i][5] * 5 + 250)
            else:
                c_ = (1550 - self.person_index[0][i][2] * 5 - self.person_index[0][i][4] * 5 -
                      (200 if self.distance_fight else 0), self.person_index[0][i][5] * 5 + 250)
            screen.blit(self.img[i], c_)

        for i in range(len(self.img_)):
            if self.tick > self.start_enemy_attack:
                c_ = (self.enemy_index[self.cadr][i][4] * 5 + (580 if self.distance_fight else 380),
                      self.enemy_index[self.cadr][i][5] * 5 + 250)
            else:
                c_ = (self.enemy_index[0][i][4] * 5 + (580 if self.distance_fight else 380),
                      self.enemy_index[0][i][5] * 5 + 250)
            screen.blit(self.img_[i], c_)
        self.person_img_id = self.person_attack_img.index(self.img)
        self.enemy_img_id = self.enemy_attack_img.index(self.img_)

        # magic
        if magic_img is not None:
            screen.blit(magic_img, (self.person_magic_cords[0] + x_, self.person_magic_cords[1] + y_)
            if self.tick < self.start_enemy_attack
            else (self.enemy_magic_cords[0] + x_, self.enemy_magic_cords[1] + y_))
            self.magic_img_id = self.all_effects.index(magic_img)
        else:
            self.magic_img_id = -1

        # miss
        if self.moves[1]:
            if (self.tick > self.person_dmg_tick) and (
                    self.tick <= self.person_dmg_tick + 40):
                screen.blit(self.miss(), (850, 300))
        if self.moves[3]:
            if (self.tick > self.enemy_dmg_tick) and (
                    self.tick <= self.enemy_dmg_tick + 40):
                screen.blit(self.miss(), (250, 300))

        # end
        if self.tick == 10 + self.person_attack_time:
            self.person_count_attack -= 1
        elif self.tick == self.start_enemy_attack + self.enemy_attack_time:
            self.enemy_count_attack -= 1

        # if self.enemy.hp <= 0 and (self.tick >= self.start_enemy_attack + ):
        #     return None
        # if self.person.hp <= 0 and (self.tick >= self.start_enemy_attack + self.enemy_attack_time + ):
        #     return None

        if self.tick == self.start_enemy_attack:
            if self.enemy_count_attack == 0 and self.person_count_attack == 0:
                return None
            elif self.enemy_count_attack == 0 and self.person_count_attack > 0:
                self.tick = 2
                self.cadr = 0
                self.script_navigator = 0
                self.cadr_tick = 0
                self.moves = [True if randint(0, 100) <= self.person.crt else False,
                              True if randint(0, 100) <= (100 - self.person_hit) else False,
                              True if randint(0, 100) <= self.enemy.crt else False,
                              True if randint(0, 100) <= (100 - self.enemy_hit) else False]

                # time
                self.person_dmg_time = self.person_times['critical' if self.moves[0] else 'attack']
                self.enemy_dmg_time = self.enemy_times['critical' if self.moves[2] else 'attack']
                self.person_attack_time = sum(
                    [i[1] for i in self.person_script['critical' if self.moves[0] else 'attack']])
                self.enemy_attack_time = sum(
                    [i[1] for i in self.enemy_script['critical' if self.moves[2] else 'attack']])
                self.start_enemy_attack = 50 + self.person_attack_time + 100

                self.person_dmg_tick = 50 + self.person_dmg_time
                self.enemy_dmg_tick = self.start_enemy_attack + self.enemy_dmg_time

                if self.person.weapon.class_ == 'magic':
                    self.end = self.start_enemy_attack + max(self.enemy_magic_effect_time, self.enemy_attack_time) + 50
                else:
                    self.end = self.start_enemy_attack + self.enemy_attack_time + 50
        else:
            if self.tick > self.end:
                if self.person_count_attack == 0 and self.enemy_count_attack == 0:
                    return None
                elif self.person_count_attack > 0:
                    self.tick = 2
                    self.cadr = 0
                    self.script_navigator = 0
                    self.cadr_tick = 0
                    self.moves = [True if randint(0, 100) <= self.person.crt else False,
                                  True if randint(0, 100) <= (100 - self.person_hit) else False,
                                  True if randint(0, 100) <= self.enemy.crt else False,
                                  True if randint(0, 100) <= (100 - self.enemy_hit) else False]

                    # time
                    self.person_dmg_time = self.person_times['critical' if self.moves[0] else 'attack']
                    self.enemy_dmg_time = self.enemy_times['critical' if self.moves[2] else 'attack']
                    self.person_attack_time = sum(
                        [i[1] for i in self.person_script['critical' if self.moves[0] else 'attack']])
                    self.enemy_attack_time = sum(
                        [i[1] for i in self.enemy_script['critical' if self.moves[2] else 'attack']])
                    self.start_enemy_attack = 50 + self.person_attack_time + 100

                    self.person_dmg_tick = 50 + self.person_dmg_time
                    self.enemy_dmg_tick = self.start_enemy_attack + self.enemy_dmg_time

                    if self.person.weapon.class_ == 'magic':
                        self.end = self.start_enemy_attack + max(self.enemy_magic_effect_time,
                                                                 self.enemy_attack_time) + 50
                    else:
                        self.end = self.start_enemy_attack + self.enemy_attack_time + 50

                elif self.enemy_count_attack > 0:
                    self.tick = self.start_enemy_attack
                    print('1')
                    self.cadr = 0
                    self.script_navigator = 0
                    self.cadr_tick = 0
                    self.moves = [True if randint(0, 100) <= self.person.crt else False,
                                  True if randint(0, 100) <= (100 - self.person_hit) else False,
                                  True if randint(0, 100) <= self.enemy.crt else False,
                                  True if randint(0, 100) <= (100 - self.enemy_hit) else False]

                    # time
                    self.person_dmg_time = self.person_times['critical' if self.moves[0] else 'attack']
                    self.enemy_dmg_time = self.enemy_times['critical' if self.moves[2] else 'attack']
                    self.person_attack_time = sum(
                        [i[1] for i in self.person_script['critical' if self.moves[0] else 'attack']])
                    self.enemy_attack_time = sum(
                        [i[1] for i in self.enemy_script['critical' if self.moves[2] else 'attack']])
                    self.start_enemy_attack = 50 + self.person_attack_time + 100

                    self.person_dmg_tick = 50 + self.person_dmg_time
                    self.enemy_dmg_tick = self.start_enemy_attack + self.enemy_dmg_time

                    if self.person.weapon.class_ == 'magic':
                        self.end = self.start_enemy_attack + max(self.enemy_magic_effect_time,
                                                                 self.enemy_attack_time) + 50
                    else:
                        self.end = self.start_enemy_attack + self.enemy_attack_time + 50
        return cords_

    def render_not_my_fight(self, screen, magic_data):
        self.tick += 1

        # fight base
        x_, y_ = self.render_base_for_fight(screen)

        # person
        for i in range(len(self.person_attack_img[self.person_img_id])):
            img = self.person_attack_img[self.person_img_id][i]
            c_ = (1550 - self.person_index[self.person_img_id][i][2] * 5 - self.person_index[self.person_img_id][i][4]
                  * 5 - (200 if self.distance_fight else 0), self.person_index[self.person_img_id][i][5] * 5 + 250)
            screen.blit(img, c_)
        # enemy
        for i in range(len(self.enemy_attack_img[self.enemy_img_id])):
            img = self.enemy_attack_img[self.enemy_img_id][i]
            c_ = c_ = (self.enemy_index[self.enemy_img_id][i][4] * 5 + (580 if self.distance_fight else 380),
                       self.enemy_index[self.enemy_img_id][i][5] * 5 + 250)
            screen.blit(img, c_)

        # magic
        id_, x__, y__ = magic_data[0], magic_data[1], magic_data[2]
        if id_ >= 0:
            screen.blit(self.all_effects[id_], (x__ + x_, y__ + y_))
