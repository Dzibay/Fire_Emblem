from settings import *
import pygame
from random import randint
from data.fight_sprites_characters import sizes, magic
from data.weapon import weapon, weapon_img, weapon_arrow, weapon_effective, weapon_have_triangle_bonus

magic_names = ['sorcerer', 'sagem']
types = {'infinite': ['lord'],
         'cavalry': ['knight_lord', 'cavalier', 'troubadour', 'valkyrie',
                     'nomad', 'nomadic_trooper'],
         'armored': ['great_lord', 'knight', 'general'],
         'swords': ['mercenary', 'hero', 'myrmidon', 'sword_master', 'blade_lord'],
         'flying': ['pegasus_knight', 'falco_knight', 'wyvern_rider', 'wyvern_lord'],
         'dragons': ['wyvern_rider', 'wyvern_lord', 'fire_dragon'],
         'nergal': ['dark_druid'],
         }


def types_class(class_):
    for type_ in types:
        if class_ in types[type_]:
            return type_


def triangle(weapon_1, weapon_2):
    if weapon_1 in weapon_have_triangle_bonus:
        return True
    else:
        if weapon_1 == weapon_2:
            return False
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

            elif weapon_1 == 'bow':
                return False
            elif weapon_2 == 'bow' and weapon_1 != 'magic':
                return True


def calculate_damage(person, enemy):
    if person.weapon in weapon_have_triangle_bonus:
        bonus = 2
    else:
        bonus = 1 if triangle(person.weapon.name, enemy.weapon.name) else -1
        if person.weapon.class_ != 'magic' or enemy.weapon.class_ != 'magic':
            if person.weapon.class_ == enemy.weapon.class_:
                bonus = 0
        else:
            if weapon[person.weapon.name]['subclass'] == weapon[enemy.weapon.name]['subclass']:
                bonus = 0

    dmg = person.mag if person.weapon.class_ == 'magic' else person.str
    dmg = (dmg + person.weapon.mt + bonus) * (2
                                              if person.weapon.name in weapon_effective[types_class(enemy.class_)]
                                              else 1)
    def_ = enemy.res if person.weapon.class_ == 'magic' else enemy.def_
    return dmg - def_


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
                    for magic_ in magic:
                        self.magic_effects[magic_] = {'person': [], 'enemy': []}
                        # enemy magic
                        self.magic_effects[magic_]['enemy'] = [pygame.transform.scale(
                            pygame.image.load(f'templates/magic/{magic_}.png').
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
                self.images[name] = {weapon: {'person': {'norm': [], 'crt': []}, 'enemy': {'norm': [], 'crt': []}}
                                     for weapon in ['sword', 'axe', 'lance', 'bow', 'magic']}
                for weapon in ['sword', 'axe', 'distance_axe', 'lance', 'distance_lance', 'bow', 'magic']:
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
    def __init__(self, person, enemy, fight_images, not_my_fight=False):
        self.fight_img = fight_images
        self.img = None
        self.person = person
        self.enemy = enemy
        self.tick = 0

        # fonts
        self.f1 = pygame.font.Font(None, 30)
        self.f2 = pygame.font.Font(None, 50)
        self.f3 = pygame.font.Font(None, 70)

        self.person_dmg = calculate_damage(person, enemy)
        self.enemy_dmg = calculate_damage(enemy, person)
        self.person_hit = person.hit + (15 if triangle(person.weapon.name, enemy.weapon.name) else -15) - enemy.avoid
        self.enemy_hit = enemy.hit + (15 if triangle(enemy.weapon.name, person.weapon.name) else -15) - person.avoid
        self.moves = [True if randint(0, 100) <= person.crt else False,
                      True if randint(0, 100) <= (100 - self.person_hit) else False,
                      True if randint(0, 100) <= enemy.crt else False,
                      True if randint(0, 100) <= (100 - self.enemy_hit) else False]
        # self.moves = [False, True, False, True]

        self.person_count_attack = 1
        self.enemy_count_attack = 1
        self.indicate_attack = 'person'
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
        self.dodge_tick = 0
        self.miss_tick = 0
        self.magic_tick = 0

        # weapon
        self.person_weapon_img = weapon_img[person.weapon.name]
        self.enemy_weapon_img = weapon_img[enemy.weapon.name]
        index_1 = self.need_moves[0] if not_my_fight else int(self.moves[0])
        index_2 = self.need_moves[1] if not_my_fight else int(self.moves[2])

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

        # baze
        self.fight_bg = pygame.image.load('templates/fight/bg.png').subsurface(1, 1, 240, 160)
        if self.distance_fight:
            self.fight_characters = pygame.image.load('templates/fight/distance_baze.png')
        else:
            self.fight_characters = pygame.image.load('templates/fight/baze.png')
        self.fight_bg = pygame.transform.scale(self.fight_bg, (WIDTH, HEIGHT))
        self.fight_characters = pygame.transform.scale(self.fight_characters, (WIDTH, HEIGHT))
        self.numbers = [pygame.transform.scale(
            pygame.image.load('templates/numbers/numbers.png').subsurface(i * 8, 0, 8, 8), (40, 40)) for i in range(10)]
        self.hp = [pygame.transform.scale(
            pygame.image.load('templates/fight/hp.png').subsurface(i * 2, 0, 2, 7), (10, 35)) for i in range(2)]

        self.miss_img = [pygame.image.load(f'templates/miss/{i}.png') for i in range(0, 12)]
        for i in range(len(self.miss_img)):
            self.miss_img[i] = pygame.transform.scale(self.miss_img[i], (100, 100))

        # persons
        person_weapon_class = person.weapon.class_
        if self.distance_fight:
            if range_persons in person.weapon.range:
                if person_weapon_class == 'axe' and 'distance_axe' in self.fight_img.images[person.name]:
                    person_weapon_class = 'distance_axe'
                elif person_weapon_class == 'lance' and 'distance_lance' in self.fight_img.images[person.name]:
                    person_weapon_class = 'distance_lance'

        self.person_melee_attack_img = self.fight_img.images[person.name][person_weapon_class]['person']['norm']
        self.person_critical_attack_img = self.fight_img.images[person.name][person_weapon_class]['person']['crt']
        self.all_person_img = self.person_melee_attack_img + self.person_critical_attack_img
        self.person_x, self.person_y = sizes[person.name][person_weapon_class][index_1]['x'], \
                                       sizes[person.name][person_weapon_class][index_1]['y']

        enemy_weapon_class = enemy.weapon.class_
        if self.distance_fight:
            if range_persons in enemy.weapon.range:
                if enemy_weapon_class == 'axe' and 'distance_axe' in self.fight_img.images[enemy.name]:
                    enemy_weapon_class = 'distance_axe'
                elif enemy_weapon_class == 'lance' and 'distance_lance' in self.fight_img.images[enemy.name]:
                    enemy_weapon_class = 'distance_lance'

        self.enemy_melee_attack_img = self.fight_img.images[enemy.name][enemy_weapon_class]['enemy']['norm']
        self.enemy_critical_attack_img = self.fight_img.images[enemy.name][enemy_weapon_class]['enemy']['crt']
        self.all_enemy_img = self.enemy_melee_attack_img + self.enemy_critical_attack_img
        self.enemy_x, self.enemy_y = sizes[enemy.name][enemy_weapon_class][index_2]['x1'], \
                                     sizes[enemy.name][enemy_weapon_class][index_2]['y']

        self.person_stay_img = self.person_critical_attack_img[0] if self.moves[0] else self.person_melee_attack_img[0]
        self.enemy_stay_img = self.enemy_critical_attack_img[0] if self.moves[2] else self.enemy_melee_attack_img[0]

        if self.distance_fight:
            self.person_x -= 200
            self.enemy_x += 200

        self.person_dmg_time = sizes[enemy.name][enemy_weapon_class][int(self.moves[2])]['dmg_time']
        self.enemy_dmg_time = sizes[person.name][person_weapon_class][int(self.moves[0])]['dmg_time']

        # attack time
        self.person_melee_attack_time = len(self.person_melee_attack_img) * 2
        self.person_critical_attack_time = len(self.person_critical_attack_img) * 2
        self.enemy_melee_attack_time = len(self.enemy_melee_attack_img) * 2
        self.enemy_critical_attack_time = len(self.enemy_critical_attack_img) * 2

        # time
        self.enemy_dmg_tick = 50 + self.enemy_dmg_time
        if not self.moves[0]:
            self.person_dmg_tick = 50 + self.person_melee_attack_time + 100 + self.person_dmg_time
            self.end = 50 + self.person_melee_attack_time + \
                       100 + self.enemy_melee_attack_time + 50
            if self.moves[2]:
                self.end = 100 + self.person_melee_attack_time + \
                           100 + self.enemy_critical_attack_time + 100
        else:
            self.person_dmg_tick = 50 + self.person_critical_attack_time + 100 + self.person_dmg_time
            self.end = 50 + self.person_critical_attack_time + \
                       100 + self.enemy_melee_attack_time + 50
            if self.moves[2]:
                self.end = 50 + self.person_critical_attack_time + \
                           100 + self.enemy_critical_attack_time + 50

        if self.moves[0]:
            self.start_enemy_attack = 50 + self.person_critical_attack_time + 100
        else:
            self.start_enemy_attack = 50 + self.person_melee_attack_time + 100

    def mellee_person_attack(self):
        self.attack_tick += 1
        img = self.person_melee_attack_img[self.attack_tick % self.person_melee_attack_time // 2]

        if self.attack_tick == self.person_melee_attack_time:
            self.attack_tick = 0

        return img

    def critical_person_attack(self):
        self.attack_tick += 1
        img = self.person_critical_attack_img[self.attack_tick % self.person_critical_attack_time // 2]

        if self.attack_tick == self.person_critical_attack_time:
            self.attack_tick = 0

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
        self.attack_tick += 1
        img = self.enemy_melee_attack_img[self.attack_tick % self.enemy_melee_attack_time // 2]

        if self.attack_tick == self.enemy_melee_attack_time:
            self.attack_tick = 0

        return img

    def critical_enemy_attack(self):
        self.attack_tick += 1
        img = self.enemy_critical_attack_img[self.attack_tick % self.enemy_critical_attack_time // 2]

        if self.attack_tick == self.enemy_critical_attack_time:
            self.attack_tick = 0

        return img

    def render_persons_characters_for_fight(self, screen):
        # bg
        screen.blit(self.fight_bg, (0, 0))
        screen.blit(self.fight_characters, (0, 0))

        # characters person
        text_name = self.f3.render(self.person.name, True, WHITE)
        screen.blit(text_name, (50, 50))

        hit = str(self.person_hit) if self.person_hit > 0 else f'0{self.person_hit}'
        dmg = str(self.person_dmg) if self.person_dmg > 9 else f'0{self.person_dmg}'
        crt = str(self.person.crt) if self.person.crt > 9 else f'0{self.person.crt}'
        for i in range(len(hit)):
            if len(hit) < 3:
                screen.blit(self.numbers[int(hit[i])], (120 + i * 40, 560))
            else:
                screen.blit(self.numbers[int(hit[i])], (80 + i * 40, 560))
        for i in range(len(dmg)):
            screen.blit(self.numbers[int(dmg[i])], (120 + i * 40, 600))
        for i in range(len(crt)):
            screen.blit(self.numbers[int(crt[i])], (120 + i * 40, 640))

        # characters enemy
        text_name = self.f3.render(self.enemy.name, True, WHITE)
        screen.blit(text_name, (1000, 50))

        hit = str(self.enemy_hit) if self.enemy_hit > 0 else f'0{self.enemy_hit}'
        dmg = str(self.enemy_dmg) if self.enemy_dmg > 9 else f'0{self.enemy_dmg}'
        crt = str(self.enemy.crt) if self.enemy.crt > 9 else f'0{self.enemy.crt}'
        for i in range(len(hit)):
            if len(hit) < 3:
                screen.blit(self.numbers[int(hit[i])], (1115 + i * 40, 560))
            else:
                screen.blit(self.numbers[int(hit[i])], (1075 + i * 40, 560))
        for i in range(len(dmg)):
            screen.blit(self.numbers[int(dmg[i])], (1115 + i * 40, 600))
        for i in range(len(crt)):
            screen.blit(self.numbers[int(crt[i])], (1115 + i * 40, 640))

        # hp
        text_hp = str(self.person.hp) if self.person.hp > 0 else '0'
        for i in range(len(text_hp)):
            screen.blit(self.numbers[int(text_hp[i])], (20 + i * 40, 725))
        for i in range(0, 2 if self.person.max_hp > 40 else 1):
            if self.person.max_hp > 40:
                for j in range(0, self.person.max_hp):
                    screen.blit(self.hp[0 if j + i * 40 < self.person.hp else 1],
                                (110 + j * 10, 705 if i == 0 else 745))
            else:
                for j in range(0, self.person.max_hp):
                    screen.blit(self.hp[0 if j + i * 40 < self.person.hp else 1],
                                (110 + j * 10, 726))

        text_hp = str(self.enemy.hp) if self.enemy.hp > 0 else '0'
        for i in range(len(text_hp)):
            screen.blit(self.numbers[int(text_hp[i])], (630 + i * 40, 725))
        for i in range(0, 2 if self.enemy.max_hp > 40 else 1):
            if self.enemy.max_hp > 40:
                for j in range(0, self.enemy.max_hp):
                    screen.blit(self.hp[0 if j + i * 40 < self.enemy.hp else 1],
                                (720 + j * 10, 705 if i == 0 else 745))
            else:
                for j in range(0, self.enemy.max_hp):
                    screen.blit(self.hp[0 if j + i * 40 < self.enemy.hp else 1],
                                (720 + j * 10, 726))

        # weapon
        screen.blit(self.person_weapon_img, (220, 608))
        screen.blit(self.enemy_weapon_img, (620, 608))
        screen.blit(self.person_weapon_arrow[self.tick % 30 // 10 if self.tick % 60 < 30 else 0], (272, 635))
        screen.blit(self.enemy_weapon_arrow[self.tick % 30 // 10 if self.tick % 60 < 30 else 0], (672, 635))
        text1 = self.f2.render(self.person.weapon.name, True, BLACK)
        text2 = self.f2.render(self.enemy.weapon.name, True, BLACK)
        screen.blit(text1, (310, 625))
        screen.blit(text2, (710, 625))

    def render_fight(self, screen):
        self.tick += 1

        if self.tick <= 50:
            img = self.person_stay_img
            img_ = self.enemy_stay_img
        else:
            if self.moves[0]:
                # person
                img = self.person_stay_img
                if self.tick <= 50 + self.person_critical_attack_time:
                    img = self.critical_person_attack()

                # enemy
                img_ = self.enemy_stay_img
                if self.moves[2]:
                    if (self.tick >= self.start_enemy_attack) and \
                            (self.tick <= self.start_enemy_attack + self.enemy_critical_attack_time):
                        img_ = self.critical_enemy_attack()
                else:
                    if (self.tick >= self.start_enemy_attack) and \
                            (self.tick <= self.start_enemy_attack + self.enemy_melee_attack_time):
                        img_ = self.mellee_enemy_attack()
            else:
                # person
                img = self.person_stay_img
                if self.tick <= 50 + self.person_melee_attack_time:
                    img = self.mellee_person_attack()

                # enemy
                img_ = self.enemy_stay_img
                if self.moves[2]:
                    if (self.tick >= self.start_enemy_attack) and \
                            (self.tick <= self.start_enemy_attack + self.enemy_critical_attack_time):
                        img_ = self.critical_enemy_attack()
                else:
                    if (self.tick >= self.start_enemy_attack) and \
                            (self.tick <= self.start_enemy_attack + self.enemy_melee_attack_time):
                        img_ = self.mellee_enemy_attack()

            # damage
            if not self.moves[3]:
                if (self.tick > self.person_dmg_tick) and (
                        self.tick < self.person_dmg_tick + 5):
                    self.person_x -= 10
                elif (self.tick > self.person_dmg_tick + 5) and (
                        self.tick < self.person_dmg_tick + 10):
                    self.person_x += 10
                if self.tick == self.person_dmg_tick + 6:
                    k_ = 3 if self.moves[2] else 1
                    self.person.damage_for_me = self.enemy_dmg * k_

            if not self.moves[1]:
                if (self.tick > self.enemy_dmg_tick) and (self.tick < self.enemy_dmg_tick + 5):
                    self.enemy_x += 10
                elif (self.tick > self.enemy_dmg_tick + 5) and (
                        self.tick < self.enemy_dmg_tick + 10):
                    self.enemy_x -= 10
                if self.tick == self.enemy_dmg_tick + 6:
                    k_ = 3 if self.moves[0] else 1
                    self.enemy.damage_for_me = self.person_dmg

            # deal damage
            for person in [self.person] + [self.enemy]:
                if person.damage_for_me > 0:
                    person.hp -= 1
                    person.damage_for_me -= 1
            if self.enemy.hp <= 0 and (self.tick >= self.start_enemy_attack):
                return None

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

        # fight baze
        self.render_persons_characters_for_fight(screen)

        # persons
        screen.blit(img, (self.person_x, self.person_y))
        screen.blit(img_, (self.enemy_x, self.enemy_y))
        self.person_img_id = self.all_person_img.index(img)
        self.enemy_img_id = self.all_enemy_img.index(img_)

        # magic
        if magic_img is not None:
            screen.blit(magic_img,
                        self.person_magic_cords if self.tick < self.start_enemy_attack
                        else self.enemy_magic_cords)
            self.magic_img_id = self.all_effects.index(magic_img)
        else:
            self.magic_img_id = -1

        # miss
        if self.moves[1]:
            if (self.tick > self.enemy_dmg_tick) and (
                    self.tick <= self.enemy_dmg_tick + 40):
                screen.blit(self.miss(), (850, 300))
        if self.moves[3]:
            if (self.tick > self.person_dmg_tick) and (
                    self.tick <= self.person_dmg_tick + 40):
                screen.blit(self.miss(), (250, 300))

        # end
        if self.tick == self.enemy_dmg_tick:
            self.person_count_attack -= 1
        elif self.tick == self.person_dmg_tick:
            self.enemy_count_attack -= 1

        if self.tick == self.start_enemy_attack:
            if self.enemy_count_attack == 0 and self.person_count_attack == 0:
                return None
            elif self.enemy_count_attack == 0 and self.person_count_attack > 0:
                self.tick = 2
                self.moves = [True if randint(0, 100) <= self.person.crt else False,
                              True if randint(0, 100) <= (100 - self.person_hit) else False,
                              True if randint(0, 100) <= self.enemy.crt else False,
                              True if randint(0, 100) <= (100 - self.enemy_hit) else False]
        else:
            if self.tick > self.end:
                if self.person_count_attack == 0 and self.enemy_count_attack == 0:
                    return None
                elif self.person_count_attack > 0:
                    self.tick = 2
                    self.moves = [True if randint(0, 100) <= self.person.crt else False,
                                  True if randint(0, 100) <= (100 - self.person_hit) else False,
                                  True if randint(0, 100) <= self.enemy.crt else False,
                                  True if randint(0, 100) <= (100 - self.enemy_hit) else False]
                elif self.enemy_count_attack > 0:
                    self.tick = self.start_enemy_attack
                    self.moves = [True if randint(0, 100) <= self.person.crt else False,
                                  True if randint(0, 100) <= (100 - self.person_hit) else False,
                                  True if randint(0, 100) <= self.enemy.crt else False,
                                  True if randint(0, 100) <= (100 - self.enemy_hit) else False]
        return cords_

    def render_not_my_fight(self, screen, magic_data):
        self.tick += 1

        if self.tick <= 2:
            self.person_x = sizes[self.person.name][self.person.weapon.class_][
                self.need_moves[0]]['x']
            self.enemy_x = sizes[self.enemy.name][self.enemy.weapon.class_][
                self.need_moves[1]]['x1']

        # fight baze
        self.render_persons_characters_for_fight(screen)

        # person
        screen.blit(self.all_person_img[self.person_img_id], (self.person_x, self.person_y))
        # enemy
        screen.blit(self.all_enemy_img[self.enemy_img_id], (self.enemy_x, self.enemy_y))

        # magic
        id_, x_, y_ = magic_data[0], magic_data[1], magic_data[2]
        if id_ >= 0:
            screen.blit(self.all_effects[id_], (x_, y_))
