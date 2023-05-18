import pygame
from person import Person, characters, weapon
from player import Player
from settings import *
from dextr import *
import socket
from fight import Fight, Fight_images, sizes, triangle, weapon_img, weapon_arrow
from random import randint


def mapping(pos):
    return (pos[0] // TILE, pos[1] // TILE)


def in_box(pos, rect):
    if pos[0] > rect[0]:
        if pos[0] < rect[0] + rect[2]:
            if pos[1] > rect[1]:
                if pos[1] < rect[1] + rect[3]:
                    return True
    return False


class Main:
    def __init__(self):
        self.start_game = False
        self.run = True
        self.your_turn = None
        self.last_sms_to_move = False
        self.tick = 0

        # pygame
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('RPG')
        self.clock = pygame.time.Clock()

        # socket
        self.server_ip = 'localhost'
        # self.server_ip = '82.146.45.210'
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.sock.connect((self.server_ip, 10000))

        # bg
        self.big_bg = pygame.image.load('templates/map/playtest_map.png')
        self.big_bg = pygame.transform.scale(self.big_bg, (1280, 1600))
        self.cam_pos = [0, 0]
        self.bg = self.big_bg.subsurface(self.cam_pos[0], self.cam_pos[1], 1200, 800)
        self.your_turn_img = pygame.image.load('templates/map/your_turn.png')
        self.opponents_turn_img = pygame.image.load('templates/map/opponents_turn.png')

        # numbers and abc
        self.numbers = [pygame.transform.scale(
            pygame.image.load('templates/numbers/numbers.png').subsurface(i * 8, 0, 8, 8), (40, 40)) for i in range(10)]

        # mouse
        self.mouse_pos = (0, 0)
        self.big_mouse_pos = (0, 0)

        # players
        self.players = [Player(), Player()]
        self.player = self.players[0]
        self.opponent = self.players[1]

        # settings unit
        self.settings_unit = False
        self.settings_unit_rect = (250, 130, 300, 300)

        # move
        self.graph, self.cant = generate_graph('levels/lvl1.txt')
        self.can_move_to = []
        self.cords = []
        self.person_positions = []
        self.person_want_move = False
        self.is_moved_in_this_turn = False

        # attack
        self.can_attack_to = []
        self.person_want_attack = False
        self.is_attacked_in_this_turn = False

        # pointer
        names_point = ['start_r', 'start_d', 'u', 'r', 'u-r', 'r-d', 'end_r', 'end_d',
                       'start_u', 'start_l', 'r', 'u', 'd-r', 'r-u', 'end_u', 'end_l']
        cords_point = [(1, 1, 16, 16), (19, 1, 16, 16), (37, 1, 16, 16), (55, 1, 16, 16),
                       (73, 1, 16, 16), (91, 1, 16, 16), (109, 1, 16, 16), (127, 1, 16, 16),
                       (1, 19, 16, 16), (19, 19, 16, 16), (37, 19, 16, 16), (55, 19, 16, 16),
                       (73, 19, 16, 16), (91, 19, 16, 16), (109, 19, 16, 16), (127, 19, 16, 16)]
        self.pointer = {names_point[i]: pygame.transform.scale(
            pygame.image.load('templates/pointer/pointer.png').subsurface(cords_point[i]), (TILE, TILE))
            for i in range(len(names_point))}

        # data
        self.data = ''
        self.magic_data = [-1, 0, 0]

        # fight
        self.without_enemy_attack = False
        self.person_double_attack = False
        self.enemy_double_attack = False
        self.fight_upload = False
        self.fight_img = None
        self.fight = False
        self.not_my_fight = False
        self.fight_person = None
        self.fight_enemy = None
        self.fight_tick = 0
        self.fight_img = Fight_images()

        # menu
        self.menu_person_settings = None
        self.menu_list_of_weapon = []
        self.menu_person_settings_exit = (700, 600, 200, 50)
        self.sms = '<wait>'
        self.menu_tick = 0
        self.menu_btn_cords = (450, 550, 300, 50)
        self.menu_person_choice_cords = [(i, j, 100, 100) for j in range(50, 530, 120) for i in range(250, 950, 120)]
        self.names_choice_persons = ['roy', 'lyn', 'marth', 'ike', 'hero',
                                     'hector', 'warrior',
                                     'eirika', 'ephraim', 'eliwood',
                                     'sorcerer', 'sagem']
        self.menu_choice_persons_weapon = {name: [characters[name]['weapon']] for name in self.names_choice_persons}
        self.menu_person_img = [
            pygame.image.load(f'templates/persons/{i}/person/map_idle.png').subsurface((0, 0, 48, 48))
            for i in self.names_choice_persons]
        for i in range(len(self.menu_person_img)):
            self.menu_person_img[i] = pygame.transform.scale(self.menu_person_img[i], (200, 200))
        self.menu_choice_persons = []

        # persons
        f_ = {i: pygame.image.load(f'templates/persons/{i}/{i}_mugshot.png') for i in self.names_choice_persons}
        self.person_faces = {i: pygame.transform.scale(f_[i], (300, 300)) for i in f_}
        self.mini_person_faces = {i: pygame.transform.scale(f_[i], (100, 100)) for i in f_}

        # placing persons
        self.placing_persons_window = False
        self.placing_choice_person = None
        self.placing_persons_pos = [(20 + i * 100, 660) for i in range(20)]

        # turn menu
        self.turn_menu = False
        self.turn_menu_rect = (20, 150, 200, 300)
        self.unit_btn = (20, 150, 200, 70)
        self.move_btn = (20, 220, 200, 70)
        self.attack_btn = (20, 290, 200, 70)
        self.wait_btn = (20, 360, 200, 70)
        self.menu_arrow = [pygame.transform.scale(pygame.image.load('templates/map/selectArrow.png').
                                                  subsurface(i * 8, 0, 8, 8), (40, 40)) for i in range(6)]

        # map person info
        self.map_person_hp = {'start': pygame.transform.scale(pygame.image.load('templates/map/map_hp.jpg').
                                                              subsurface(0, 0, 7, 7), (15, 15)),
                              '1': pygame.transform.scale(pygame.image.load('templates/map/map_hp.jpg').
                                                          subsurface(8, 0, 7, 7), (15, 15)),
                              '0': pygame.transform.scale(pygame.image.load('templates/map/map_hp.jpg').
                                                          subsurface(16, 0, 7, 7), (15, 15)),
                              'end': pygame.transform.scale(pygame.image.load('templates/map/map_hp.jpg').
                                                            subsurface(24, 0, 7, 7), (15, 15))}
        self.fight_info = pygame.transform.scale(pygame.image.load('templates/map/fight_info.png'), (300, 450))

        # map highlight
        self.highlight = {
            'blue': [pygame.transform.scale(pygame.image.load('templates/highlights/blue.png').
                                            subsurface(i * 16, 1, 15, 15), (TILE, TILE)) for i in range(16)],
            'red': [pygame.transform.scale(pygame.image.load('templates/highlights/red.png').
                                           subsurface(i * 16, 1, 15, 15), (TILE, TILE)) for i in range(16)]}

        # cursor
        self.cursor = {'norm': [pygame.transform.scale(pygame.image.load('templates/map/cursor.png').
                                                       subsurface((x * 32, 0, 32, 32)), (TILE, TILE))
                                for x in range(4)],
                       'enemy': [pygame.transform.scale(pygame.image.load('templates/map/cursor.png').
                                                        subsurface((x * 32, 32, 32, 32)), (TILE, TILE))
                                 for x in range(4)],
                       'none': [pygame.transform.scale(pygame.image.load('templates/map/cursor.png').
                                                       subsurface((x * 32, 64, 32, 32)), (TILE, TILE))
                                for x in range(4)],
                       'heal': [pygame.transform.scale(pygame.image.load('templates/map/cursor.png').
                                                       subsurface((x * 32, 96, 32, 32)), (TILE, TILE))
                                for x in range(4)]}

        # fonts
        self.f1 = pygame.font.Font(None, 30)
        self.f2 = pygame.font.Font(None, 50)
        self.f3 = pygame.font.Font(None, 70)

        self.font = [pygame.transform.scale(pygame.image.load('templates/fonts/text.png').
                                            subsurface(x * 5, 0, 5, 7), (30, 30)) for x in range(26)]

    def write(self, s, pos):
        self.screen.blit(self.font[0], pos)

    @staticmethod
    def find_sms(s):
        first = None
        for i in range(len(s)):
            if s[i] == '|':
                first = i
            if s[i] == '>' and first is not None:
                end = i
                res = s[first + 1:end].split(',')
                res = [i.split(' ') for i in res if len(i) > 0]
                result = [(i[0], int(i[1]), int(i[2]), i[3], int(i[4]), int(i[5]), int(i[6]), int(i[7]), i[8]) for i in
                          res]
                return result
        return None

    @staticmethod
    def is_fight(s):
        first = None
        for i in range(len(s)):
            if s[i] == '<':
                first = i
            if s[i] == '>' and first is not None:
                end = i
                res = s[first:end][:6]
                if res[:6] == '<fight':
                    return True
        return False

    @staticmethod
    def find_fight_magic(s):
        first = None
        for i in range(len(s)):
            if s[i] == '<':
                first = i
            if s[i] == '|' and first is not None:
                end = i
                res = s[first + 1:end][6:].split(' ')
                res = [int(i) for i in res]
                return res
        return ''

    @staticmethod
    def find_fight(s):
        first = None
        for i in range(len(s)):
            if s[i] == '|':
                first = i
            if s[i] == '>' and first is not None:
                end = i
                res = s[first + 1:end].split(',')
                res = [[int(i) for i in j.split(' ')] for j in res]
                return res
        return ''

    @staticmethod
    def find_persons_images(s):
        first = None
        for i in range(len(s)):
            if s[i] == '|':
                first = i
            if s[i] == '>' and first is not None:
                end = i
                res = s[first + 1:end - 1].split(' ')
                return res
        return ''

    def get_can_to(self, pos, l, not_append=None):
        if not_append is None:
            not_append = []
        res = [(x, y)
               for x in range(pos[0] - l[len(l) - 1], pos[0] + l[len(l) - 1] + 1) if x >= 0
               for y in range(pos[1] - l[len(l) - 1], pos[1] + l[len(l) - 1] + 1) if y >= 0]
        result = []
        for i in res:
            cords = get_cords(self.graph, pos, i)
            if (i not in self.cant) and (i not in not_append) and (len(cords) - 1 in l):
                result.append(i)
        return result

    def render_persons_characters_for_fight(self, fight):
        # bg
        self.screen.blit(fight.fight_bg, (0, 0))
        self.screen.blit(fight.fight_characters, (0, 0))

        # characters person
        text_name = self.f3.render(self.fight_person.name, True, WHITE)
        self.screen.blit(text_name, (50, 50))

        hit = str(fight.person_hit) if fight.person_hit > 0 else f'0{fight.person_hit}'
        dmg = str(fight.person_dmg) if fight.person_dmg > 9 else f'0{fight.person_dmg}'
        crt = str(self.fight_person.crt) if self.fight_person.crt > 9 else f'0{self.fight_person.crt}'
        for i in range(len(hit)):
            if len(hit) < 3:
                self.screen.blit(fight.numbers[int(hit[i])], (120 + i * 40, 560))
            else:
                self.screen.blit(fight.numbers[int(hit[i])], (80 + i * 40, 560))
        for i in range(len(dmg)):
            self.screen.blit(fight.numbers[int(dmg[i])], (120 + i * 40, 600))
        for i in range(len(crt)):
            self.screen.blit(fight.numbers[int(crt[i])], (120 + i * 40, 640))

        # characters enemy
        text_name = self.f3.render(self.fight_enemy.name, True, WHITE)
        self.screen.blit(text_name, (1000, 50))

        hit = str(fight.enemy_hit) if fight.enemy_hit > 0 else f'0{fight.enemy_hit}'
        dmg = str(fight.enemy_dmg) if fight.enemy_dmg > 9 else f'0{fight.enemy_dmg}'
        crt = str(self.fight_enemy.crt) if self.fight_enemy.crt > 9 else f'0{self.fight_enemy.crt}'
        for i in range(len(hit)):
            if len(hit) < 3:
                self.screen.blit(fight.numbers[int(hit[i])], (1115 + i * 40, 560))
            else:
                self.screen.blit(fight.numbers[int(hit[i])], (1075 + i * 40, 560))
        for i in range(len(dmg)):
            self.screen.blit(fight.numbers[int(dmg[i])], (1115 + i * 40, 600))
        for i in range(len(crt)):
            self.screen.blit(fight.numbers[int(crt[i])], (1115 + i * 40, 640))

        # hp
        text_hp = str(self.fight_person.hp) if self.fight_person.hp > 0 else '0'
        for i in range(len(text_hp)):
            self.screen.blit(fight.numbers[int(text_hp[i])], (20 + i * 40, 725))
        for i in range(0, 2 if self.fight_person.max_hp > 40 else 1):
            if self.fight_person.max_hp > 40:
                for j in range(0, self.fight_person.max_hp):
                    self.screen.blit(fight.hp[0 if j + i * 40 < self.fight_person.hp else 1],
                                     (110 + j * 10, 705 if i == 0 else 745))
            else:
                for j in range(0, self.fight_person.max_hp):
                    self.screen.blit(fight.hp[0 if j + i * 40 < self.fight_person.hp else 1],
                                     (110 + j * 10, 726))

        text_hp = str(self.fight_enemy.hp) if self.fight_enemy.hp > 0 else '0'
        for i in range(len(text_hp)):
            self.screen.blit(fight.numbers[int(text_hp[i])], (630 + i * 40, 725))
        for i in range(0, 2 if self.fight_enemy.max_hp > 40 else 1):
            if self.fight_enemy.max_hp > 40:
                for j in range(0, self.fight_enemy.max_hp):
                    self.screen.blit(fight.hp[0 if j + i * 40 < self.fight_enemy.hp else 1],
                                     (720 + j * 10, 705 if i == 0 else 745))
            else:
                for j in range(0, self.fight_enemy.max_hp):
                    self.screen.blit(fight.hp[0 if j + i * 40 < self.fight_enemy.hp else 1],
                                     (720 + j * 10, 726))

        # weapon
        self.screen.blit(fight.person_weapon_img, (220, 608))
        self.screen.blit(fight.enemy_weapon_img, (620, 608))
        self.screen.blit(fight.person_weapon_arrow[self.tick % 30 // 10 if self.tick % 60 < 30 else 0], (272, 635))
        self.screen.blit(fight.enemy_weapon_arrow[self.tick % 30 // 10 if self.tick % 60 < 30 else 0], (672, 635))

    def render_fight(self):
        global fight
        self.fight_tick += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False

        if self.fight_tick == 1:
            fight = Fight(self.fight_person, self.fight_enemy, self.fight_img)

        enemy_dmg_tick = 50 + fight.enemy_dmg_tick
        if not fight.moves[0]:
            person_dmg_tick = 50 + fight.person_melee_attack_time + 100 + fight.person_dmg_tick
            fight_end = 50 + fight.person_melee_attack_time + \
                        100 + fight.enemy_melee_attack_time + 50
            if fight.moves[2]:
                fight_end = 100 + fight.person_melee_attack_time + \
                            100 + fight.enemy_critical_attack_time + 100
        else:
            person_dmg_tick = 50 + fight.person_critical_attack_time + 100 + fight.person_dmg_tick
            fight_end = fight_end = 50 + fight.person_critical_attack_time + \
                                    100 + fight.enemy_melee_attack_time + 50
            if fight.moves[2]:
                person_dmg_tick = 1110
                fight_end = fight_end = 50 + fight.person_critical_attack_time + \
                                        100 + fight.enemy_critical_attack_time + 50

        start_enemy_attack = 1000
        if self.fight_tick <= 50:
            img = fight.person_stay_img
            img_ = fight.enemy_stay_img
        else:
            if fight.moves[0]:
                # person
                img = fight.person_stay_img
                if self.fight_tick <= 50 + fight.person_critical_attack_time:
                    img = fight.critical_person_attack()

                # enemy
                img_ = fight.enemy_stay_img
                start_enemy_attack = 50 + fight.person_critical_attack_time + 100
                if fight.moves[2]:
                    if (self.fight_tick >= start_enemy_attack) and \
                            (self.fight_tick <= start_enemy_attack + fight.enemy_critical_attack_time):
                        img_ = fight.critical_enemy_attack()
                else:
                    if (self.fight_tick >= start_enemy_attack) and \
                            (self.fight_tick <= start_enemy_attack + fight.enemy_melee_attack_time):
                        img_ = fight.mellee_enemy_attack()
            else:
                # person
                img = fight.person_stay_img
                if self.fight_tick <= 50 + fight.person_melee_attack_time:
                    img = fight.mellee_person_attack()

                # enemy
                img_ = fight.enemy_stay_img
                start_enemy_attack = 50 + fight.person_melee_attack_time + 100
                if fight.moves[2]:
                    if (self.fight_tick >= start_enemy_attack) and \
                            (self.fight_tick <= start_enemy_attack + fight.enemy_critical_attack_time):
                        img_ = fight.critical_enemy_attack()
                else:
                    if (self.fight_tick >= start_enemy_attack) and \
                            (self.fight_tick <= start_enemy_attack + fight.enemy_melee_attack_time):
                        img_ = fight.mellee_enemy_attack()

            # damage
            if not fight.moves[3]:
                if (self.fight_tick > person_dmg_tick) and (self.fight_tick < person_dmg_tick + 5):
                    fight.person_x -= 10
                elif (self.fight_tick > person_dmg_tick + 5) and (self.fight_tick < person_dmg_tick + 10):
                    fight.person_x += 10
                if self.fight_tick == person_dmg_tick + 6:
                    k_ = 3 if fight.moves[2] else 1
                    self.fight_person.damage_for_me = fight.enemy_dmg * k_

            if not fight.moves[1]:
                if (self.fight_tick > enemy_dmg_tick) and (self.fight_tick < enemy_dmg_tick + 5):
                    fight.enemy_x += 10
                elif (self.fight_tick > enemy_dmg_tick + 5) and (self.fight_tick < enemy_dmg_tick + 10):
                    fight.enemy_x -= 10
                if self.fight_tick == enemy_dmg_tick + 6:
                    k_ = 3 if fight.moves[0] else 1
                    self.fight_enemy.damage_for_me = fight.person_dmg * k_

            # deal damage
            for person in [self.fight_person] + [self.fight_enemy]:
                if person.damage_for_me > 0:
                    person.hp -= 1
                    person.damage_for_me -= 1
            if self.fight_enemy.hp <= 0 and (self.fight_tick >= start_enemy_attack):
                self.fight_tick = 0
                self.fight = False

        # magic effect
        magic_img = None
        if self.fight_person.weapon in self.fight_img.magic_effects:
            if (self.fight_tick > 55 + fight.person_magic_delay) and \
                    (self.fight_tick <= 55 + fight.person_magic_delay + fight.person_magic_effect_time):
                fight.magic_tick += 1
                magic_img = fight.person_magic_effect[fight.magic_tick % fight.person_magic_effect_time // 2]
                if self.fight_tick == 55 + fight.person_magic_delay + fight.person_magic_effect_time:
                    fight.magic_tick = 0
                    magic_img = None

        if self.fight_enemy.weapon in self.fight_img.magic_effects:
            if (self.fight_tick > start_enemy_attack + fight.enemy_magic_delay) and \
                    (self.fight_tick <= start_enemy_attack + fight.enemy_magic_delay + fight.enemy_magic_effect_time):
                fight.magic_tick += 1
                magic_img = fight.enemy_magic_effect[fight.magic_tick % fight.enemy_magic_effect_time // 2]
                if self.fight_tick == start_enemy_attack + fight.enemy_magic_delay + fight.enemy_magic_effect_time:
                    fight.magic_tick = 0
                    magic_img = None

        if self.fight_tick < start_enemy_attack:
            cords_ = fight.person_magic_cords_sms
        else:
            cords_ = fight.enemy_magic_cords_sms

        # send sms
        sms = f'<fight {fight.magic_img_id} {cords_[0]} {cords_[1]}|' \
              f'{self.opponent.persons.index(self.fight_enemy)} {fight.person_img_id} ' \
              f'{int(fight.moves[0])} {int(fight.person_y)} {self.fight_person.hp},' \
              f'{self.player.persons.index(self.fight_person)} {fight.enemy_img_id} ' \
              f'{int(fight.moves[2])} {int(fight.enemy_y)} {self.fight_enemy.hp}>'
        self.sock.send(sms.encode())

        # recv sms
        try:
            self.data = self.sock.recv(1024).decode()
            self.not_my_fight = False
        except:
            pass

        # fight baze
        main.render_persons_characters_for_fight(fight)

        # persons
        self.screen.blit(img, (fight.person_x, fight.person_y))
        self.screen.blit(img_, (fight.enemy_x, fight.enemy_y))
        fight.person_img_id = fight.all_person_img.index(img)
        fight.enemy_img_id = fight.all_enemy_img.index(img_)

        # magic
        if magic_img is not None:
            if self.fight_tick < start_enemy_attack:
                cords = fight.person_magic_cords
            else:
                cords = fight.enemy_magic_cords
            self.screen.blit(magic_img, cords)
            fight.magic_img_id = fight.all_effects.index(magic_img)
        else:
            fight.magic_img_id = -1

        # miss
        if fight.moves[1]:
            if (self.fight_tick > 50 + fight.person_dmg_tick) and (
                    self.fight_tick <= 50 + fight.person_dmg_tick + 40):
                self.screen.blit(fight.miss(), (850, 300))
        if fight.moves[3]:
            if (self.fight_tick > start_enemy_attack + fight.enemy_dmg_tick) and (
                    self.fight_tick <= start_enemy_attack + fight.enemy_dmg_tick + 40):
                self.screen.blit(fight.miss(), (250, 300))

        # end
        if fight.indicate_double_attack:
            if fight.person_double_attack and self.fight_tick >= start_enemy_attack:
                self.fight_tick = 0
                self.fight = False
            elif fight.enemy_double_attack and self.fight_tick >= fight_end:
                self.fight_tick = 0
                self.fight = False
        elif fight.without_enemy_attack and self.fight_tick >= start_enemy_attack:
            self.fight_tick = 0
            self.fight = False
        elif self.fight_tick > fight_end:
            fight.indicate_double_attack = True
            if fight.person_double_attack and self.fight_person.hp > 0:
                self.fight_tick = 5
                fight.moves[0] = True if randint(0, 100) <= self.fight_person.crt else False
                fight.moves[1] = True if randint(0, 100) <= (1 - fight.person_hit) else False
            elif fight.enemy_double_attack and self.fight_person.hp > 0:
                self.fight_tick = start_enemy_attack
                fight.moves[2] = True if randint(0, 100) <= self.fight_enemy.crt else False
                fight.moves[3] = True if randint(0, 100) <= (1 - fight.enemy_hit) else False
            else:
                self.fight_tick = 0
                self.fight = False

    def render_not_my_fight(self):
        global fight
        self.fight_tick += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False

        if not self.fight_upload:
            fight = Fight(self.fight_person, self.fight_enemy, self.fight_img, True)
            self.fight_upload = True

        # recv sms
        try:
            self.data = self.sock.recv(1024).decode()
            if main.is_fight(self.data):
                self.magic_data = main.find_fight_magic(self.data)
                self.data = main.find_fight(self.data)
                id_1, fight.person_img_id, fight.need_moves[0], fight.person_y, self.fight_person.hp = self.data[1]
                id_2, fight.enemy_img_id, fight.need_moves[1], fight.enemy_y, self.fight_enemy.hp = self.data[0]
                if self.fight_person.hp <= 0:
                    self.player.persons.remove(self.fight_person)
            else:
                self.not_my_fight = False
                self.data = main.find_sms(self.data)
                if len(self.data) != len(self.opponent.persons):
                    self.opponent.persons = [Person(j[1], j[2], j[0]) for j in self.data]
                for j in range(len(self.data)):
                    self.opponent.persons[j].x = self.data[j][1]
                    self.opponent.persons[j].y = self.data[j][2]
        except:
            pass

        # fight baze
        main.render_persons_characters_for_fight(fight)

        # person
        self.screen.blit(fight.all_person_img[fight.person_img_id],
                         (fight.person_x, fight.person_y))
        # enemy
        self.screen.blit(fight.all_enemy_img[fight.enemy_img_id],
                         (fight.enemy_x, fight.enemy_y))

        # magic
        id_, x_, y_ = self.magic_data[0], self.magic_data[1], self.magic_data[2]
        if id_ >= 0:
            self.screen.blit(fight.all_effects[id_], (x_, y_))

    def render(self):
        mouse_pos = (self.mouse_pos[0] + self.cam_pos[0],
                     self.mouse_pos[1] + self.cam_pos[1])
        # bg
        self.screen.blit(self.bg, (0, 0))

        # mouse
        pygame.draw.rect(self.screen, BLACK, (self.mouse_pos[0] * TILE, self.mouse_pos[1] * TILE, TILE, TILE), 1)

        # person move
        if self.person_want_move:
            try:
                p_ = self.player.persons[self.player.choice_person]
                pygame.draw.rect(self.screen, ORANGE, (p_.get_big_pos()[0] - self.cam_pos[0] * TILE,
                                                       p_.get_big_pos()[1] - self.cam_pos[1] * TILE, TILE, TILE), 3)

                # can move to
                for i in self.can_move_to:
                    self.screen.blit(self.highlight['blue'][self.tick % 80 // 5],
                                     ((i[0] - self.cam_pos[0]) * TILE, (i[1] - self.cam_pos[1]) * TILE))

                # pointer
                if mouse_pos in self.can_move_to:
                    self.cords = get_cords(self.graph, p_.pos, mouse_pos)
                    for i in range(len(self.cords) - 1):
                        img = None
                        if i == 0:
                            if self.cords[i][0] < self.cords[i + 1][0]:
                                img = 'end_l'
                            elif self.cords[i][0] > self.cords[i + 1][0]:
                                img = 'end_r'
                            elif self.cords[i][1] < self.cords[i + 1][1]:
                                img = 'end_u'
                            elif self.cords[i][1] > self.cords[i + 1][1]:
                                img = 'end_d'
                        else:
                            if (self.cords[i - 1][0] < self.cords[i][0] and self.cords[i][1] < self.cords[i + 1][1]) or \
                                    (self.cords[i + 1][0] < self.cords[i][0] and self.cords[i][1] < self.cords[i - 1][
                                        1]):
                                img = 'r-d'
                            elif (self.cords[i - 1][0] < self.cords[i][0] and self.cords[i][1] > self.cords[i + 1][
                                1]) or \
                                    (self.cords[i + 1][0] < self.cords[i][0] and self.cords[i][1] > self.cords[i - 1][
                                        1]):
                                img = 'r-u'
                            elif (self.cords[i - 1][0] > self.cords[i][0] and self.cords[i][1] < self.cords[i + 1][
                                1]) or \
                                    (self.cords[i + 1][0] > self.cords[i][0] and self.cords[i][1] < self.cords[i - 1][
                                        1]):
                                img = 'u-r'
                            elif (self.cords[i - 1][0] > self.cords[i][0] and self.cords[i][1] > self.cords[i + 1][
                                1]) or \
                                    (self.cords[i + 1][0] > self.cords[i][0] and self.cords[i][1] > self.cords[i - 1][
                                        1]):
                                img = 'd-r'
                            else:
                                if i == len(self.cords) - 2:
                                    if self.cords[i][0] < self.cords[i + 1][0]:
                                        img = 'start_l'
                                    elif self.cords[i][0] > self.cords[i + 1][0]:
                                        img = 'start_r'
                                    elif self.cords[i][1] < self.cords[i + 1][1]:
                                        img = 'start_u'
                                    elif self.cords[i][1] > self.cords[i + 1][1]:
                                        img = 'start_d'
                        if img is None:
                            if self.cords[i - 1][0] < self.cords[i][0] or self.cords[i - 1][0] > self.cords[i][0]:
                                img = 'r'
                            else:
                                img = 'u'
                        if img is not None:
                            self.screen.blit(self.pointer[img], ((self.cords[i][0] - self.cam_pos[0]) * TILE,
                                                                 (self.cords[i][1] - self.cam_pos[1]) * TILE))
            except:
                self.player.choice_person = None

        # person_attack
        if self.person_want_attack:
            for i in self.can_attack_to:
                self.screen.blit(self.highlight['red'][self.tick % 80 // 5],
                                 ((i[0] - self.cam_pos[0]) * TILE, (i[1] - self.cam_pos[1]) * TILE))

        # persons
        for person in self.player.persons:
            # person move
            self.cords = person.move(self.cords)

            # person img
            choice_ = False
            try:
                if person == self.player.persons[self.player.choice_person]:
                    choice_ = True
            except:
                pass
            person.choice_image(self.tick, choice_)

        for player in self.players:
            for i in range(len(player.persons)):
                if player == self.opponent:
                    try:
                        # opponent persons img
                        if self.data[i][3] == 'stay':
                            if self.tick % 120 < 40:
                                i_ = (self.tick % 40 // 10)
                            else:
                                i_ = 0
                            self.opponent.persons[i].img = self.opponent.persons[i].enemy_stay_images[i_]
                        elif self.data[i][3] == 'move_L':
                            self.opponent.persons[i].img = self.opponent.persons[i].enemy_move_left_images[
                                self.tick % 40 // 10]
                        elif self.data[i][3] == 'move_R':
                            self.opponent.persons[i].img = self.opponent.persons[i].enemy_move_right_images[
                                self.tick % 40 // 10]
                        elif self.data[i][3] == 'move_D':
                            self.opponent.persons[i].img = self.opponent.persons[i].enemy_move_down_images[
                                self.tick % 40 // 10]
                        elif self.data[i][3] == 'move_U':
                            self.opponent.persons[i].img = self.opponent.persons[i].enemy_move_up_images[
                                self.tick % 40 // 10]
                    except:
                        print('cant print')
                # person blit
                if (player.persons[i].pos[0] >= self.cam_pos[0]) and \
                        (player.persons[i].pos[0] <= self.cam_pos[0] + 15) and \
                        (player.persons[i].pos[1] >= self.cam_pos[1]) and \
                        (player.persons[i].pos[1] <= self.cam_pos[1] + 10):
                    self.screen.blit(player.persons[i].img,
                                     (player.persons[i].x - self.cam_pos[0] * TILE - 88,
                                      player.persons[i].y - self.cam_pos[1] * TILE - 100))

        if len(self.menu_choice_persons) == 0:
            # turn menu
            if self.turn_menu:
                pygame.draw.rect(self.screen, BLUE, self.turn_menu_rect)

                choice_rect = pygame.Surface((200, 30))
                choice_rect.fill(GREY)
                choice_rect.set_alpha(80)
                if in_box(self.big_mouse_pos, self.unit_btn):
                    self.screen.blit(choice_rect, (self.unit_btn[0], self.unit_btn[1] + 20))
                    self.screen.blit(self.menu_arrow[self.tick % 12 // 2 if self.tick % 36 < 12 else 0],
                                     (self.unit_btn[0] + 150, self.unit_btn[1] + 15))
                elif in_box(self.big_mouse_pos, self.move_btn):
                    self.screen.blit(choice_rect, (self.move_btn[0], self.move_btn[1] + 20))
                    self.screen.blit(self.menu_arrow[self.tick % 12 // 2 if self.tick % 36 < 12 else 0],
                                     (self.move_btn[0] + 150, self.move_btn[1] + 15))
                elif in_box(self.big_mouse_pos, self.attack_btn):
                    self.screen.blit(choice_rect, (self.attack_btn[0], self.attack_btn[1] + 20))
                    self.screen.blit(self.menu_arrow[self.tick % 12 // 2 if self.tick % 36 < 12 else 0],
                                     (self.attack_btn[0] + 150, self.attack_btn[1] + 15))
                elif in_box(self.big_mouse_pos, self.wait_btn):
                    self.screen.blit(choice_rect, (self.wait_btn[0], self.wait_btn[1] + 20))
                    self.screen.blit(self.menu_arrow[self.tick % 12 // 2 if self.tick % 36 < 12 else 0],
                                     (self.wait_btn[0] + 150, self.wait_btn[1] + 15))

                pygame.draw.rect(self.screen, WHITE, self.turn_menu_rect, 5)

                text_unit = self.f2.render('Unit', True, WHITE)
                text_move = self.f2.render('Move', True, WHITE)
                text_attack = self.f2.render('Attack', True, WHITE)
                text_wait = self.f2.render('Wait', True, WHITE)
                self.screen.blit(text_unit, (self.unit_btn[0] + 50, self.unit_btn[1] + 19))
                self.screen.blit(text_move, (self.move_btn[0] + 50, self.move_btn[1] + 19))
                self.screen.blit(text_attack, (self.attack_btn[0] + 35, self.attack_btn[1] + 19))
                self.screen.blit(text_wait, (self.wait_btn[0] + 50, self.wait_btn[1] + 19))

            # see person info
            for person in self.player.persons + self.opponent.persons:
                if mouse_pos == person.pos:
                    # rect
                    pygame.draw.rect(self.screen, SKY_BLUE, (20, 680, 260, 100))
                    self.screen.blit(self.mini_person_faces[person.name], (20, 680))
                    pygame.draw.rect(self.screen, WHITE, (20, 680, 260, 100), 3)

                    # name
                    text_name = self.f2.render(person.name, True, BLACK)
                    self.screen.blit(text_name, (140, 685))

                    # hp
                    text_hp = self.f2.render('HP', True, BLACK)
                    text_person_hp = self.f2.render(f'{person.hp}/{person.max_hp}', True, BLACK)
                    self.screen.blit(text_hp, (125, 725))
                    self.screen.blit(text_person_hp, (185, 725))

                    for i in range(10):
                        if i == 0:
                            img_ = self.map_person_hp['start']
                        elif i == 9 and 100 / person.max_hp * person.hp > 90:
                            img_ = self.map_person_hp['end']
                        elif (i - 1) * 10 < 100 / person.max_hp * person.hp:
                            img_ = self.map_person_hp['1']
                        else:
                            img_ = self.map_person_hp['0']
                        self.screen.blit(img_, (122 + 15 * i, 760))

        # person placing window
        if self.placing_persons_window:
            pygame.draw.rect(self.screen, BLUE, (0, 650, WIDTH, 150))
            for i in range(len(self.menu_choice_persons)):
                img = self.menu_person_img[self.menu_choice_persons[i]]
                self.screen.blit(img, (self.placing_persons_pos[i][0] - 50, self.placing_persons_pos[i][1] - 50))
            if self.placing_choice_person is not None:
                pos_ = self.placing_persons_pos[self.menu_choice_persons.index(self.placing_choice_person)]
                pygame.draw.rect(self.screen, WHITE, (pos_[0], pos_[1], 100, 100), 2)

        # indicate turn
        self.screen.blit(self.your_turn_img if self.your_turn else self.opponents_turn_img, (500, 0))

        # fps
        text_fps = self.f1.render(str(self.clock.get_fps()), True, BLACK)
        self.screen.blit(text_fps, (1150, 0))

        # settings person
        if self.settings_unit:
            # info person
            p_ = self.player.persons[self.player.choice_person]
            self.screen.blit(self.person_faces[p_.name], (750, 150))
            pygame.draw.rect(self.screen, BLUE, (700, 450, 400, 300))
            pygame.draw.rect(self.screen, WHITE, (700, 450, 400, 300), 5)

            text_name = self.f3.render(p_.name, True, WHITE)
            self.screen.blit(text_name, (750, 470))

            pygame.draw.rect(self.screen, WHITE, (1020, 458, 72, 72))
            self.screen.blit(weapon_img[p_.weapon], (1015, 453))

            # weapon
            pygame.draw.rect(self.screen, BLUE, self.settings_unit_rect)
            pygame.draw.rect(self.screen, WHITE, self.settings_unit_rect, 5)
            for i in range(len(self.menu_choice_persons_weapon[p_.name])):
                pygame.draw.rect(self.screen, WHITE, (260, 140 + i * 80, 280, 72))
                self.screen.blit(weapon_img[self.menu_choice_persons_weapon[p_.name][i]], (255, 135 + i * 80))

        # info for attack
        if self.person_want_attack:
            for enemy in self.opponent.persons:
                if in_box(self.big_mouse_pos, (enemy.get_big_pos()[0], enemy.get_big_pos()[1], TILE, TILE)):
                    self.screen.blit(self.fight_info, (875, 100))
                    p_ = self.player.persons[self.player.choice_person]
                    f = pygame.font.Font(None, 60)

                    # person
                    person_name = self.f2.render(p_.name, True, WHITE)
                    self.screen.blit(person_name, (1005, 140))
                    self.screen.blit(weapon_img[p_.weapon], (875, 105))
                    self.screen.blit(weapon_arrow['up' if triangle(p_.weapon, enemy.weapon) else 'down']
                                     [self.tick % 30 // 10 if self.tick % 60 < 30 else 0], (920, 130))
                    print(triangle(p_.weapon, enemy.weapon))
                    person_hp = f.render(str(p_.hp), True, WHITE)
                    person_mt = f.render(str(p_.weapon_mt), True, WHITE)
                    person_hit = f.render(str(p_.hit), True, WHITE)
                    person_crt = f.render(str(p_.crt), True, WHITE)
                    self.screen.blit(person_hp, (1100, 185))
                    self.screen.blit(person_mt, (1100, 245))
                    self.screen.blit(person_hit, (1100, 305))
                    self.screen.blit(person_crt, (1100, 365))

                    # enemy
                    enemy_name = self.f2.render(enemy.name, True, WHITE)
                    self.screen.blit(enemy_name, (940, 440))
                    self.screen.blit(weapon_img[enemy.weapon], (1090, 400))
                    self.screen.blit(weapon_arrow['up' if triangle(enemy.weapon, p_.weapon) else 'down']
                                     [self.tick % 30 // 10 if self.tick % 60 < 30 else 0], (1135, 440))
                    enemy_hp = f.render(str(enemy.hp), True, WHITE)
                    enemy_mt = f.render(str(enemy.weapon_mt), True, WHITE)
                    enemy_hit = f.render(str(enemy.hit), True, WHITE)
                    enemy_crt = f.render(str(enemy.crt), True, WHITE)
                    self.screen.blit(enemy_hp, (900, 185))
                    self.screen.blit(enemy_mt, (900, 245))
                    self.screen.blit(enemy_hit, (900, 305))
                    self.screen.blit(enemy_crt, (900, 365))

    def place_persons(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_TAB:
                    if self.placing_persons_window:
                        self.placing_persons_window = False
                    else:
                        self.placing_persons_window = True
                else:
                    if event.key == pygame.K_w:
                        if self.cam_pos[1] > 0:
                            self.cam_pos[1] -= 1
                    elif event.key == pygame.K_s:
                        if self.cam_pos[1] + 10 < 20:
                            self.cam_pos[1] += 1
                    elif event.key == pygame.K_d:
                        if self.cam_pos[0] + 15 < 16:
                            self.cam_pos[0] += 1
                    elif event.key == pygame.K_a:
                        if self.cam_pos[0] > 0:
                            self.cam_pos[0] -= 1
                    self.bg = self.big_bg.subsurface(self.cam_pos[0] * TILE,
                                                     self.cam_pos[1] * TILE, 1200, 800)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.placing_persons_window:
                    for i in range(len(self.menu_choice_persons)):
                        if in_box(self.big_mouse_pos,
                                  (self.placing_persons_pos[i][0], self.placing_persons_pos[i][1], 100, 100)):
                            if self.placing_choice_person != self.menu_choice_persons[i]:
                                self.placing_choice_person = self.menu_choice_persons[i]
                            else:
                                self.placing_choice_person = None
                else:
                    self.person_positions = [i.pos for i in self.opponent.persons + self.player.persons]
                    mouse_pos = (self.mouse_pos[0] + self.cam_pos[0],
                                 self.mouse_pos[1] + self.cam_pos[1])
                    if (self.placing_choice_person is not None) and \
                            (mouse_pos not in self.person_positions + self.cant):
                        name_ = self.names_choice_persons[self.placing_choice_person]
                        self.player.persons.append(Person(self.mouse_pos[0] * TILE + self.cam_pos[0] * TILE,
                                                          self.mouse_pos[1] * TILE + self.cam_pos[1] * TILE,
                                                          name_, self.menu_choice_persons_weapon[name_][0]))
                        self.menu_choice_persons.remove(self.placing_choice_person)
                        self.placing_choice_person = None

        sms = f'<{self.your_turn}|'
        for person in self.player.persons:
            sms += f'{person.name} {person.x} {person.y} {person.state}{person.move_to} ' \
                   f'{person.hp} {person.hit} {person.dmg} {person.crt} {person.weapon},'
        sms += '>'
        self.sock.send(sms.encode())

        # recv sms
        try:
            data_ = self.sock.recv(1024).decode()
            if data_ == '<wait>':
                self.start_game = False
            self.data = main.find_sms(data_)
            if len(self.data) != len(self.opponent.persons):
                if [(j[1] // TILE, j[2] // TILE) for j in self.data] != \
                        [person.pos for person in self.player.persons]:
                    self.opponent.persons = [Person(j[1], j[2], j[0]) for j in self.data]

            for j in range(len(self.data)):
                self.opponent.persons[j].x = self.data[j][1]
                self.opponent.persons[j].y = self.data[j][2]
                self.opponent.persons[j].pos = (self.data[j][1] // TILE,
                                                self.data[j][2] // TILE)
                self.opponent.persons[j].hp = self.data[j][4]
                self.opponent.persons[j].hit = self.data[j][5]
                self.opponent.persons[j].dmg = self.data[j][6]
                self.opponent.persons[j].crt = self.data[j][7]
                w_ = self.opponent.persons[j].weapon
                self.opponent.persons[j].weapon = self.data[j][8]
                if self.opponent.persons[j].weapon != w_:
                    self.opponent.persons[j].change_weapon()
        except:
            pass

    def menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            elif self.sms[:8] != '<my_pers':
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    # person settings
                    if self.menu_person_settings is not None:
                        if in_box(self.big_mouse_pos, self.menu_person_settings_exit):
                            self.menu_person_settings = None
                        else:
                            # weapon choice
                            for i in range(len(self.menu_list_of_weapon)):
                                if in_box(self.big_mouse_pos, (600, 200 + i * 75, 200, 72)):
                                    l_ = self.menu_choice_persons_weapon[self.names_choice_persons[
                                        self.menu_person_settings]]
                                    if self.menu_list_of_weapon[i] not in l_:
                                        l_.append(self.menu_list_of_weapon[i])
                                    else:
                                        l_.remove(self.menu_list_of_weapon[i])
                    # start
                    elif in_box(self.big_mouse_pos, self.menu_btn_cords):
                        self.menu_choice_persons = [self.menu_person_choice_cords.index(j) for j in
                                                    self.menu_choice_persons]
                        self.menu_choice_persons = [i for i in self.menu_choice_persons if
                                                    i < len(self.menu_person_img)]
                        print(self.menu_choice_persons)
                        self.placing_persons_window = True
                        self.menu_choice_persons_weapon = {
                            self.names_choice_persons[i]: self.menu_choice_persons_weapon[
                                self.names_choice_persons[i]]
                            for i in self.menu_choice_persons}
                        self.sms = f'<my_pers |'
                        for i in self.menu_choice_persons:
                            self.sms += self.names_choice_persons[i] + ','
                        self.sms += '>'
                    else:
                        # add/remove person
                        for i in self.menu_person_choice_cords:
                            if in_box(self.big_mouse_pos, i):
                                if i in self.menu_choice_persons:
                                    self.menu_choice_persons.remove(i)
                                else:
                                    self.menu_choice_persons.append(i)
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                    for i in self.menu_person_choice_cords:
                        if in_box(self.big_mouse_pos, i):
                            self.menu_person_settings = self.menu_person_choice_cords.index(i)
                            self.menu_list_of_weapon = [j for j in weapon if weapon[j]['class'] in sizes[
                                self.names_choice_persons[self.menu_person_settings]]]
                            self.menu_choice_persons.append(i)

        data_ = self.sock.recv(1024).decode()
        if data_[:5] == '<wait' and data_[:6] != '<wait>':
            self.fight_img.uppload_images(self.names_choice_persons[i] for i in self.menu_choice_persons)
            data_ = main.find_persons_images(data_)
            self.fight_img.uppload_images(data_)
            self.start_game = True
            self.sms = '<ready>'
        elif data_[1:10].split(' ')[0] in self.names_choice_persons:
            self.start_game = True
        self.sock.send(self.sms.encode())

        # draw
        self.screen.fill(GREY)
        if self.sms[:8] != '<my_pers':
            # person settings
            if self.menu_person_settings is not None:
                text_name = self.f3.render(self.names_choice_persons[self.menu_person_settings], True, WHITE)
                self.screen.blit(text_name, (500, 100))
                pygame.draw.rect(self.screen, RED, self.menu_person_settings_exit)
                # person list weapon
                l_ = self.menu_choice_persons_weapon[self.names_choice_persons[self.menu_person_settings]]
                for i in range(len(l_)):
                    pygame.draw.rect(self.screen, WHITE, (300, 200 + i * 75, 200, 72))
                    self.screen.blit(weapon_img[l_[i]], (300, 195 + i * 75))
                # list all weapon
                for i in range(len(self.menu_list_of_weapon)):
                    c_ = BLACK if self.menu_list_of_weapon[i] in l_ else WHITE
                    pygame.draw.rect(self.screen, c_, (600, 200 + i * 75, 200, 72))
                    self.screen.blit(weapon_img[self.menu_list_of_weapon[i]], (600, 195 + i * 75))
            else:
                for i in range(len(self.menu_person_choice_cords)):
                    c_ = BLUE if self.menu_person_choice_cords[i] in self.menu_choice_persons else WHITE
                    pygame.draw.rect(self.screen, c_, self.menu_person_choice_cords[i])
                    try:
                        self.screen.blit(self.menu_person_img[i],
                                         (self.menu_person_choice_cords[i][0] - 50,
                                          self.menu_person_choice_cords[i][1] - 50))
                    except:
                        pass
                pygame.draw.rect(self.screen, GREEN, self.menu_btn_cords)
        else:
            self.menu_tick += 1
            i_ = self.menu_tick % 160 // 20
            if i_ == 1:
                cords = [(WIDTH // 2 - 50, HEIGHT // 2 - 50, 50, 50)]
            elif i_ == 2:
                cords = [(WIDTH // 2 - 50, HEIGHT // 2 - 50, 50, 50),
                         (WIDTH // 2, HEIGHT // 2, 50, 50)]
            elif i_ == 3:
                cords = [(WIDTH // 2 - 50, HEIGHT // 2 - 50, 50, 50),
                         (WIDTH // 2, HEIGHT // 2 - 50, 50, 50),
                         (WIDTH // 2, HEIGHT // 2, 50, 50)]
            elif i_ == 4:
                cords = [(WIDTH // 2 - 50, HEIGHT // 2 - 50, 50, 50),
                         (WIDTH // 2, HEIGHT // 2 - 50, 50, 50),
                         (WIDTH // 2, HEIGHT // 2, 50, 50),
                         (WIDTH // 2 - 50, HEIGHT // 2, 50, 50)]
            elif i_ == 5:
                cords = [(WIDTH // 2, HEIGHT // 2 - 50, 50, 50),
                         (WIDTH // 2, HEIGHT // 2, 50, 50),
                         (WIDTH // 2 - 50, HEIGHT // 2, 50, 50)]
            elif i_ == 6:
                cords = [(WIDTH // 2, HEIGHT // 2 - 50, 50, 50),
                         (WIDTH // 2 - 50, HEIGHT // 2, 50, 50)]
            elif i_ == 7:
                cords = [(WIDTH // 2 - 50, HEIGHT // 2, 50, 50)]
            else:
                cords = []

            for i in cords:
                pygame.draw.rect(self.screen, WHITE, i)
            text = self.f1.render('Waiting the second player...', True, WHITE)
            self.screen.blit(text, (WIDTH // 2 - 140, HEIGHT // 2 + 70))
        pygame.display.update()

    def main_loop(self):
        while self.run:
            self.tick += 1
            self.clock.tick(FPS)
            self.big_mouse_pos = pygame.mouse.get_pos()
            self.mouse_pos = mapping(pygame.mouse.get_pos())
            if self.start_game:
                if self.fight:
                    main.render_fight()
                elif self.not_my_fight:
                    main.render_not_my_fight()
                else:
                    if len(self.menu_choice_persons) == 0:
                        # events
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                self.run = False
                            if event.type == pygame.KEYUP:
                                if event.key == pygame.K_e:
                                    self.your_turn = True
                                    self.is_moved_in_this_turn = False
                                else:
                                    if event.key == pygame.K_w:
                                        if self.cam_pos[1] > 0:
                                            self.cam_pos[1] -= 1
                                    elif event.key == pygame.K_s:
                                        if self.cam_pos[1] + 10 < 20:
                                            self.cam_pos[1] += 1
                                    elif event.key == pygame.K_d:
                                        if self.cam_pos[0] + 15 < 16:
                                            self.cam_pos[0] += 1
                                    elif event.key == pygame.K_a:
                                        if self.cam_pos[0] > 0:
                                            self.cam_pos[0] -= 1
                                    self.bg = self.big_bg.subsurface(self.cam_pos[0] * TILE,
                                                                     self.cam_pos[1] * TILE, 1200, 800)

                            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                                if self.settings_unit:
                                    if in_box(self.big_mouse_pos, self.settings_unit_rect):
                                        p_ = self.player.persons[self.player.choice_person]
                                        for i in range(len(self.menu_choice_persons_weapon[p_.name])):
                                            r_ = (260, 140 + i * 80, 280, 72)
                                            if in_box(self.big_mouse_pos, r_):
                                                p_.weapon = self.menu_choice_persons_weapon[p_.name][i]
                                                p_.change_weapon()
                                    else:
                                        self.settings_unit = False
                                else:
                                    if self.your_turn:
                                        mouse_pos = (self.mouse_pos[0] + self.cam_pos[0],
                                                     self.mouse_pos[1] + self.cam_pos[1])
                                        if self.player.choice_person is not None:
                                            # person choice none
                                            if mouse_pos == self.player.persons[self.player.choice_person].pos:
                                                self.player.choice_person = None
                                            else:
                                                # turn menu
                                                if self.turn_menu:
                                                    p_ = self.player.persons[self.player.choice_person]
                                                    if in_box(self.big_mouse_pos, self.unit_btn):
                                                        self.settings_unit = True
                                                    elif in_box(self.big_mouse_pos, self.move_btn) and \
                                                            not self.is_moved_in_this_turn:
                                                        self.person_want_move = True
                                                        self.person_positions = [person.pos
                                                                                 for person in self.opponent.persons]
                                                        self.can_move_to = main.get_can_to(p_.pos, [i for i in range(
                                                            p_.movement)],
                                                                                           self.person_positions)
                                                        self.turn_menu = False
                                                    elif in_box(self.big_mouse_pos, self.attack_btn) and \
                                                            not self.is_attacked_in_this_turn:
                                                        self.person_want_attack = True
                                                        self.can_attack_to = main.get_can_to(p_.pos, p_.range_attack,
                                                                                             [p_.pos])
                                                        self.turn_menu = False
                                                    elif in_box(self.big_mouse_pos, self.wait_btn):
                                                        self.your_turn = False
                                                        self.turn_menu = False
                                                else:
                                                    # move
                                                    if self.person_want_move and mouse_pos in self.can_move_to:
                                                        self.player.persons[
                                                            self.player.choice_person].want_move = mouse_pos
                                                        self.is_moved_in_this_turn = True
                                                        self.player.choice_person = None

                                                    # attack
                                                    elif self.person_want_attack and mouse_pos in self.can_attack_to:
                                                        for enemy in self.opponent.persons:
                                                            if mouse_pos == enemy.pos:
                                                                self.fight_tick = 0
                                                                self.fight_person = self.player.persons[
                                                                    self.player.choice_person]
                                                                self.fight_enemy = enemy
                                                                self.fight = True
                                                                self.is_attacked_in_this_turn = True
                                                                self.is_moved_in_this_turn = True
                                                                self.player.choice_person = None

                                        else:
                                            # choice person
                                            for person in self.player.persons:
                                                if mouse_pos == person.pos:
                                                    if self.player.choice_person is None:
                                                        self.player.choice_person = self.player.persons.index(person)
                                                        self.turn_menu = True
                        if self.player.choice_person is None:
                            self.turn_menu = False
                            self.person_want_move = False
                            self.person_want_attack = False

                        # send sms
                        sms = f'<{self.your_turn}|'
                        for person in self.player.persons:
                            sms += f'{person.name} {person.x} {person.y} {person.state}{person.move_to} ' \
                                   f'{person.hp} {person.hit} {person.dmg} {person.crt} {person.weapon},'
                        sms += '>'
                        self.sock.send(sms.encode())

                        # recv sms
                        try:
                            data_ = self.sock.recv(1024).decode()
                            if data_[:5] == '<True':
                                self.your_turn = True
                            elif data_[:6] == '<False':
                                self.your_turn = False
                            if self.your_turn != self.last_sms_to_move:
                                self.is_moved_in_this_turn = False
                                self.is_attacked_in_this_turn = False
                                self.player.choice_person = None
                            self.last_sms_to_move = self.your_turn
                            if data_ == '<wait>':
                                pass
                            if main.is_fight(data_):
                                self.data = main.find_fight(data_)
                                self.not_my_fight = True
                                self.fight_upload = False
                                id_1, a_, b_, c_, d_ = self.data[1]
                                id_2, a_, b_, c_, d_ = self.data[0]
                                self.fight_person = self.player.persons[id_2]
                                self.fight_enemy = self.opponent.persons[id_1]

                            else:
                                self.not_my_fight = False
                                self.data = main.find_sms(data_)
                                if len(self.data) != len(self.opponent.persons):
                                    if [(j[1] // TILE, j[2] // TILE) for j in self.data] != \
                                            [person.pos for person in self.player.persons]:
                                        self.opponent.persons = [Person(j[1], j[2], j[0]) for j in self.data]

                                for j in range(len(self.data)):
                                    self.opponent.persons[j].x = self.data[j][1]
                                    self.opponent.persons[j].y = self.data[j][2]
                                    self.opponent.persons[j].pos = (self.data[j][1] // TILE,
                                                                    self.data[j][2] // TILE)
                                    self.opponent.persons[j].hp = self.data[j][4]
                                    self.opponent.persons[j].hit = self.data[j][5]
                                    self.opponent.persons[j].dmg = self.data[j][6]
                                    self.opponent.persons[j].crt = self.data[j][7]
                                    w_ = self.opponent.persons[j].weapon
                                    self.opponent.persons[j].weapon = self.data[j][8]
                                    if self.opponent.persons[j].weapon != w_:
                                        self.opponent.persons[j].change_weapon()

                        except:
                            pass

                        # attack
                        for person in self.player.persons:
                            a_ = []
                            b_ = []
                            for enemy in self.opponent.persons:
                                if abs(person.pos[0] - enemy.pos[0]) + \
                                        abs(person.pos[1] - enemy.pos[1]) in person.range_attack:
                                    a_.append(enemy)
                                    b_.append((enemy.pos[0] * TILE + TILE, enemy.pos[1] * TILE - (TILE / 2), 100, 30))
                                else:
                                    pass
                            person.can_fight_with = a_
                            person.attack_button = b_

                        # dead persons
                        for player in self.players:
                            for person in player.persons:
                                if person.hp <= 0:
                                    player.persons.remove(person)
                    else:
                        main.place_persons()
                    if self.not_my_fight:
                        pass
                    else:

                        if self.start_game:
                            main.render()
                pygame.display.update()
            else:
                main.menu()


main = Main()

main.main_loop()
pygame.quit()
