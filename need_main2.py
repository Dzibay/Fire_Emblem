import pygame
import socket
from person import Person, characters
from player import Player
from settings import *
from dextr import *
from fight import Fight, Fight_images, triangle
from menu import Menu
from data.weapon import weapon, weapon_img, weapon_arrow, weapon_can_be_used


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
        self.fight = None
        self.start_game = False
        self.run = True
        self.your_turn = None
        self.last_sms_to_move = False
        self.tick = 0
        self.choice_person = None
        self.fight_flag = False

        # pygame
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('RPG')
        self.clock = pygame.time.Clock()

        self.menu = Menu(self.screen)

        # socket
        self.server_ip = 'localhost'
        # self.server_ip = '82.146.45.210'
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.sock.connect((self.server_ip, 10000))

        # bg
        self.big_bg = pygame.image.load('templates/map/playtest_map.png')
        self.big_bg = pygame.transform.scale(self.big_bg, (TILE * 16, TILE * 20))
        self.cam_pos = [0, 0]
        self.bg = self.big_bg.subsurface(self.cam_pos[0], self.cam_pos[1], TILE * 16, 1040)
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
        self.turn_phase = 'move'

        # attack
        self.can_attack_to = []
        self.person_want_attack = False

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
        self.sms = '<wait>'
        self.magic_data = [-1, 0, 0]

        # fight
        self.fight_flag = False
        self.not_my_fight = False
        self.fight_img = Fight_images()

        # persons
        f_ = {i: pygame.image.load(f'templates/persons/{i}/{i}_mugshot.png') for i in self.menu.all_names_persons}
        self.person_faces = {i: pygame.transform.scale(f_[i], (300, 300)) for i in f_}
        self.mini_person_faces = {i: pygame.transform.scale(f_[i], (100, 100)) for i in f_}

        # placing persons
        self.placing_persons_window = False
        self.placing_choice_person = None
        self.placing_persons_pos = [(20 + i * 100, 660) for i in range(20)]

        # turn menu
        self.turn_menu = False
        self.turn_menu_rect = (20, 150, 200, 300)
        self.unit_btn = None
        self.move_btn = (20, 150, 200, 70)
        self.attack_btn = None
        self.wait_btn = (20, 220, 200, 70)
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
        pass

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
                return res
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

    @staticmethod
    def list_of_weapon_can_be_used_by_person(person_name, person_class):
        res = []
        for weapon_ in weapon:
            if weapon[weapon_]['class'] in characters[person_name]['can_use']:
                if weapon_ in weapon_can_be_used:
                    if (person_name in weapon_can_be_used[weapon_]) or (person_class in weapon_can_be_used[weapon_]):
                        res.append(weapon_)
                else:
                    res.append(weapon_)
        return res

    def events(self, flag):
        if flag == 'main':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        if self.cam_pos[1] > 0:
                            self.cam_pos[1] -= 1
                    elif event.key == pygame.K_s:
                        if self.cam_pos[1] + 13 < 20:
                            self.cam_pos[1] += 1
                    elif event.key == pygame.K_d:
                        if self.cam_pos[0] + 16 < 16:
                            self.cam_pos[0] += 1
                    elif event.key == pygame.K_a:
                        if self.cam_pos[0] > 0:
                            self.cam_pos[0] -= 1
                    self.bg = self.big_bg.subsurface(self.cam_pos[0] * TILE,
                                                     self.cam_pos[1] * TILE, TILE * 16, 1040)

                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if self.settings_unit:
                        if in_box(self.big_mouse_pos, self.settings_unit_rect):
                            p_ = self.player.persons[self.choice_person]
                            for i in range(len(self.menu.choice_persons_weapon[p_.name])):
                                r_ = (260, 140 + i * 80, 280, 72)
                                if in_box(self.big_mouse_pos, r_):
                                    p_.change_weapon(self.menu.choice_persons_weapon[p_.name][i])
                        else:
                            self.settings_unit = False
                    else:
                        if self.your_turn:
                            mouse_pos = (self.mouse_pos[0] + self.cam_pos[0],
                                         self.mouse_pos[1] + self.cam_pos[1])
                            if self.choice_person is not None:
                                # person choice none
                                if mouse_pos == self.player.persons[self.choice_person].pos:
                                    self.choice_person = None
                                else:
                                    # turn menu
                                    if self.turn_menu:
                                        p_ = self.player.persons[self.choice_person]
                                        # move phase
                                        if self.turn_phase == 'move':
                                            if in_box(self.big_mouse_pos, self.move_btn) and \
                                                    self.turn_phase == 'move':
                                                self.person_want_move = True
                                                self.person_positions = [person.pos
                                                                         for person in
                                                                         self.opponent.persons]
                                                self.can_move_to = self.get_can_to(p_.pos,
                                                                                   [i for i in range(
                                                                                       p_.movement)],
                                                                                   self.person_positions)
                                                self.turn_menu = False
                                            elif in_box(self.big_mouse_pos, self.wait_btn):
                                                self.turn_phase = 'attack'

                                        # attack phase
                                        elif self.turn_phase == 'attack':
                                            if in_box(self.big_mouse_pos, self.unit_btn):
                                                self.settings_unit = True
                                            elif in_box(self.big_mouse_pos, self.attack_btn):
                                                self.person_want_attack = True
                                                self.can_attack_to = self.get_can_to(p_.pos,
                                                                                     p_.weapon.range,
                                                                                     [p_.pos])
                                                self.turn_menu = False
                                            elif in_box(self.big_mouse_pos, self.wait_btn):
                                                self.your_turn = False
                                                self.turn_menu = False
                                    else:
                                        # move
                                        if self.person_want_move and mouse_pos in self.can_move_to:
                                            self.player.persons[self.choice_person].want_move = mouse_pos
                                            self.turn_phase = 'attack'
                                            self.choice_person = None

                                        # attack
                                        elif self.person_want_attack and mouse_pos in self.can_attack_to:
                                            for enemy in self.opponent.persons:
                                                if mouse_pos == enemy.pos:
                                                    self.fight_flag = True
                                                    self.fight = Fight(self.player.persons[self.choice_person], enemy,
                                                                       self.fight_img)
                                                    self.your_turn = False
                                                    self.turn_phase = 'move'
                                                    print('yeee')
                                                    self.choice_person = None

                            else:
                                # choice person
                                for person in self.player.persons:
                                    if mouse_pos == person.pos:
                                        if self.choice_person is None:
                                            self.choice_person = self.player.persons.index(person)
                                            self.turn_menu = True
        elif flag == 'menu':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                elif self.sms[:8] != '<my_pers':
                    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        # person settings
                        if self.menu.person_settings is not None:
                            if in_box(self.big_mouse_pos, self.menu.settings_exit_btn):
                                self.menu.person_settings = None
                            else:
                                # weapon choice
                                for i in range(5):
                                    if in_box(self.big_mouse_pos, (600, 200 + i * 75, 200, 72)):
                                        l_ = self.menu.choice_persons_weapon[self.menu.all_names_persons[
                                            self.menu.person_settings]]
                                        weapon_ = self.menu.list_of_weapon[
                                                  self.menu.list_of_weapon_see:self.menu.list_of_weapon_see + 5][i]
                                        if weapon_ not in l_:
                                            if len(l_) < 3:
                                                l_.append(weapon_)
                                        else:
                                            l_.remove(weapon_)
                        # start
                        elif in_box(self.big_mouse_pos, self.menu.start_btn):
                            self.menu.choice_persons = [self.menu.person_choice_cords.index(j) for j in
                                                        self.menu.choice_persons]
                            self.menu.choice_persons = [i for i in self.menu.choice_persons if
                                                        i < len(self.menu.person_faces)]
                            self.placing_persons_window = True
                            self.menu.choice_persons_weapon = {
                                self.menu.all_names_persons[i]: self.menu.choice_persons_weapon[
                                    self.menu.all_names_persons[i]]
                                for i in self.menu.choice_persons}
                            self.sms = f'<my_pers |'
                            for i in self.menu.choice_persons:
                                self.sms += self.menu.all_names_persons[i] + ','
                            self.sms += '>'
                        else:
                            # menu phase
                            if in_box(self.big_mouse_pos, self.menu.edit_team_btn):
                                self.menu.phase = 'edit_team'
                            if in_box(self.big_mouse_pos, self.menu.ally_growth_btn):
                                if len(self.menu.choice_persons) > 0:
                                    self.menu.phase = 'ally_growth'
                                    self.menu.ally_growth_person = self.menu.all_names_persons[
                                        self.menu.person_choice_cords.index(self.menu.choice_persons[0])]
                            if in_box(self.big_mouse_pos, self.menu.equipment_btn):
                                self.menu.phase = 'equipment'

                            # add/remove person
                            if self.menu.phase == 'edit_team':
                                for i in self.menu.person_choice_cords:
                                    if in_box(self.big_mouse_pos, i):
                                        if i in self.menu.choice_persons:
                                            self.menu.choice_persons.remove(i)
                                        else:
                                            if len(self.menu.choice_persons) < 5:
                                                self.menu.choice_persons.append(i)
                            if self.menu.phase == 'ally_growth':
                                if in_box(self.big_mouse_pos, self.menu.lvl_up_btn):
                                    if self.menu.result_person_stats[self.menu.ally_growth_person]['lvl'] + self.menu.up_lvl < 20:
                                        self.menu.up_lvl += 1
                                elif in_box(self.big_mouse_pos, self.menu.lvl_down_btn):
                                    if self.menu.up_lvl > 0:
                                        self.menu.up_lvl -= 1
                                elif in_box(self.big_mouse_pos, self.menu.lvl_result_btn):
                                    self.menu.change_lvl()
                                    self.menu.result_person_stats[self.menu.ally_growth_person]['lvl'] += self.menu.up_lvl
                                    self.menu.up_lvl = 0
                                else:
                                    for i in range(len(self.menu.choice_persons)):
                                        if in_box(self.big_mouse_pos, (1165 + i * 90, 120, 100, 100)):
                                            self.menu.ally_growth_person = self.menu.all_names_persons[
                                                self.menu.person_choice_cords.index(self.menu.choice_persons[i])]

                    elif event.type == pygame.MOUSEBUTTONUP and event.button == 3 and \
                            self.menu.person_settings is None:
                        for i in range(len(self.menu.person_choice_cords)):
                            if in_box(self.big_mouse_pos, self.menu.person_choice_cords[i]):
                                self.menu.person_settings = i
                                class_ = characters[self.menu.all_names_persons[i]]['class']
                                self.menu.list_of_weapon = self.list_of_weapon_can_be_used_by_person(
                                    self.menu.all_names_persons[i], class_)
                                self.menu.list_of_weapon_see = 0
                    elif event.type == pygame.KEYUP:
                        if event.key == pygame.K_UP:
                            if self.menu.list_of_weapon_see > 0:
                                self.menu.list_of_weapon_see -= 1
                        if event.key == pygame.K_DOWN:
                            if self.menu.list_of_weapon_see < len(self.menu.list_of_weapon) - 5:
                                self.menu.list_of_weapon_see += 1
        else:
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
                            if self.cam_pos[1] + 13 < 20:
                                self.cam_pos[1] += 1
                        elif event.key == pygame.K_d:
                            if self.cam_pos[0] + 16 < 16:
                                self.cam_pos[0] += 1
                        elif event.key == pygame.K_a:
                            if self.cam_pos[0] > 0:
                                self.cam_pos[0] -= 1
                        self.bg = self.big_bg.subsurface(self.cam_pos[0] * TILE,
                                                         self.cam_pos[1] * TILE, TILE * 16, 1040)
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if self.placing_persons_window:
                        for i in range(len(self.menu.choice_persons)):
                            if in_box(self.big_mouse_pos,
                                      (self.placing_persons_pos[i][0], self.placing_persons_pos[i][1], 100,
                                       100)):
                                if self.placing_choice_person != self.menu.choice_persons[i]:
                                    self.placing_choice_person = self.menu.choice_persons[i]
                                else:
                                    self.placing_choice_person = None
                    else:
                        self.person_positions = [i.pos for i in self.opponent.persons + self.player.persons]
                        mouse_pos = (self.mouse_pos[0] + self.cam_pos[0],
                                     self.mouse_pos[1] + self.cam_pos[1])
                        if (self.placing_choice_person is not None) and \
                                (mouse_pos not in self.person_positions + self.cant):
                            name_ = self.menu.all_names_persons[self.placing_choice_person]
                            self.player.persons.append(
                                Person(self.mouse_pos[0] * TILE + self.cam_pos[0] * TILE,
                                       self.mouse_pos[1] * TILE + self.cam_pos[1] * TILE,
                                       name_, self.menu.result_person_stats[name_],
                                       self.menu.choice_persons_weapon[name_][0]))
                            self.menu.choice_persons.remove(self.placing_choice_person)
                            self.placing_choice_person = None

    def render(self):
        mouse_pos = (self.mouse_pos[0] + self.cam_pos[0],
                     self.mouse_pos[1] + self.cam_pos[1])
        # bg
        self.screen.fill(BLACK)
        self.screen.blit(self.bg, (0, 0))

        # mouse
        pygame.draw.rect(self.screen, BLACK, (self.mouse_pos[0] * TILE, self.mouse_pos[1] * TILE, TILE, TILE), 1)

        # person move
        if self.person_want_move:
            try:
                p_ = self.player.persons[self.choice_person]
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
                self.choice_person = None

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
                if person == self.player.persons[self.choice_person]:
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
                            self.opponent.persons[i].move_to = ''
                            self.opponent.persons[i].img = self.opponent.persons[i].map_images[
                                self.opponent.persons[i].weapon.class_]['enemy']['stand'][i_]
                        else:
                            self.opponent.persons[i].move_to = self.data[i][3]
                            self.opponent.persons[i].img = \
                                self.opponent.persons[i].map_images[
                                    self.opponent.persons[i].weapon.class_]['enemy'][self.data[i][3]][self.tick % 40 // 10]
                    except:
                        print('cant print')

                # person blit
                if (player.persons[i].pos[0] >= self.cam_pos[0]) and \
                        (player.persons[i].pos[0] <= self.cam_pos[0] + 15) and \
                        (player.persons[i].pos[1] >= self.cam_pos[1]) and \
                        (player.persons[i].pos[1] <= self.cam_pos[1] + 10):
                    offset = (135, 140) if player.persons[i].move_to == '' else (100, 150)
                    self.screen.blit(player.persons[i].img,
                                     (player.persons[i].x - self.cam_pos[0] * TILE - offset[0],
                                      player.persons[i].y - self.cam_pos[1] * TILE - offset[1]))

        if len(self.menu.choice_persons) == 0:
            # turn menu
            if self.turn_menu:
                pygame.draw.rect(self.screen, BLUE, self.turn_menu_rect)

                choice_rect = pygame.Surface((200, 30))
                choice_rect.fill(GREY)
                choice_rect.set_alpha(80)

                if self.unit_btn is not None and in_box(self.big_mouse_pos, self.unit_btn):
                    self.screen.blit(choice_rect, (self.unit_btn[0], self.unit_btn[1] + 20))
                    self.screen.blit(self.menu_arrow[self.tick % 12 // 2 if self.tick % 36 < 12 else 0],
                                     (self.unit_btn[0] + 150, self.unit_btn[1] + 15))
                elif self.move_btn is not None and in_box(self.big_mouse_pos, self.move_btn):
                    self.screen.blit(choice_rect, (self.move_btn[0], self.move_btn[1] + 20))
                    self.screen.blit(self.menu_arrow[self.tick % 12 // 2 if self.tick % 36 < 12 else 0],
                                     (self.move_btn[0] + 150, self.move_btn[1] + 15))
                elif self.attack_btn is not None and in_box(self.big_mouse_pos, self.attack_btn):
                    self.screen.blit(choice_rect, (self.attack_btn[0], self.attack_btn[1] + 20))
                    self.screen.blit(self.menu_arrow[self.tick % 12 // 2 if self.tick % 36 < 12 else 0],
                                     (self.attack_btn[0] + 150, self.attack_btn[1] + 15))
                elif self.wait_btn is not None and in_box(self.big_mouse_pos, self.wait_btn):
                    self.screen.blit(choice_rect, (self.wait_btn[0], self.wait_btn[1] + 20))
                    self.screen.blit(self.menu_arrow[self.tick % 12 // 2 if self.tick % 36 < 12 else 0],
                                     (self.wait_btn[0] + 150, self.wait_btn[1] + 15))

                pygame.draw.rect(self.screen, WHITE, self.turn_menu_rect, 5)

                text_unit = self.f2.render('Unit', True, WHITE)
                text_move = self.f2.render('Move', True, WHITE)
                text_attack = self.f2.render('Attack', True, WHITE)
                text_wait = self.f2.render('Wait', True, WHITE)
                if self.unit_btn is not None:
                    self.screen.blit(text_unit, (self.unit_btn[0] + 50, self.unit_btn[1] + 19))
                if self.move_btn is not None:
                    self.screen.blit(text_move, (self.move_btn[0] + 50, self.move_btn[1] + 19))
                if self.attack_btn is not None:
                    self.screen.blit(text_attack, (self.attack_btn[0] + 35, self.attack_btn[1] + 19))
                if self.wait_btn is not None:
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
            for i in range(len(self.menu.choice_persons)):
                img = self.menu.person_faces[self.menu.choice_persons[i]]
                self.screen.blit(img, (self.placing_persons_pos[i][0], self.placing_persons_pos[i][1]))
            if self.placing_choice_person is not None:
                pos_ = self.placing_persons_pos[self.menu.choice_persons.index(self.placing_choice_person)]
                pygame.draw.rect(self.screen, WHITE, (pos_[0], pos_[1], 100, 100), 2)

        # indicate turn
        self.screen.blit(self.your_turn_img if self.your_turn else self.opponents_turn_img, (500, 0))

        # settings person
        if self.settings_unit:
            # info person
            p_ = self.player.persons[self.choice_person]
            self.screen.blit(self.person_faces[p_.name], (750, 150))
            pygame.draw.rect(self.screen, BLUE, (700, 450, 400, 300))
            pygame.draw.rect(self.screen, WHITE, (700, 450, 400, 300), 5)

            text_name = self.f3.render(p_.name, True, WHITE)
            self.screen.blit(text_name, (750, 470))

            pygame.draw.rect(self.screen, WHITE, (1020, 458, 72, 72))
            self.screen.blit(weapon_img[p_.weapon.name], (1015, 453))

            # weapon
            pygame.draw.rect(self.screen, BLUE, self.settings_unit_rect)
            pygame.draw.rect(self.screen, WHITE, self.settings_unit_rect, 5)
            for i in range(len(self.menu.choice_persons_weapon[p_.name])):
                pygame.draw.rect(self.screen, WHITE, (260, 140 + i * 80, 280, 72))
                self.screen.blit(weapon_img[self.menu.choice_persons_weapon[p_.name][i]], (255, 135 + i * 80))

        # info for attack
        if self.person_want_attack:
            for enemy in self.opponent.persons:
                if in_box(self.big_mouse_pos, (enemy.get_big_pos()[0], enemy.get_big_pos()[1], TILE, TILE)):
                    self.screen.blit(self.fight_info, (875, 100))
                    p_ = self.player.persons[self.choice_person]
                    f = pygame.font.Font(None, 60)

                    # person
                    person_name = self.f2.render(p_.name, True, WHITE)
                    self.screen.blit(person_name, (1005, 140))
                    self.screen.blit(weapon_img[p_.weapon.name], (875, 105))
                    self.screen.blit(weapon_arrow['up' if triangle(p_.weapon.name, enemy.weapon.name) else 'down']
                                     [self.tick % 30 // 10 if self.tick % 60 < 30 else 0], (920, 130))
                    person_hp = f.render(str(p_.hp), True, WHITE)
                    person_mt = f.render(str(p_.weapon.mt), True, WHITE)
                    person_hit = f.render(str(p_.hit), True, WHITE)
                    person_crt = f.render(str(p_.crt), True, WHITE)
                    self.screen.blit(person_hp, (1100, 185))
                    self.screen.blit(person_mt, (1100, 245))
                    self.screen.blit(person_hit, (1100, 305))
                    self.screen.blit(person_crt, (1100, 365))

                    # enemy
                    enemy_name = self.f2.render(enemy.name, True, WHITE)
                    self.screen.blit(enemy_name, (940, 440))
                    self.screen.blit(weapon_img[enemy.weapon.name], (1090, 400))
                    self.screen.blit(weapon_arrow['up' if triangle(enemy.weapon.name, p_.weapon.name) else 'down']
                                     [self.tick % 30 // 10 if self.tick % 60 < 30 else 0], (1135, 440))
                    enemy_hp = f.render(str(enemy.hp), True, WHITE)
                    enemy_mt = f.render(str(enemy.weapon.mt), True, WHITE)
                    enemy_hit = f.render(str(enemy.hit), True, WHITE)
                    enemy_crt = f.render(str(enemy.crt), True, WHITE)
                    self.screen.blit(enemy_hp, (900, 185))
                    self.screen.blit(enemy_mt, (900, 245))
                    self.screen.blit(enemy_hit, (900, 305))
                    self.screen.blit(enemy_crt, (900, 365))

    def main_loop(self):
        while self.run:
            self.tick += 1
            self.clock.tick(FPS)
            self.big_mouse_pos = pygame.mouse.get_pos()
            self.mouse_pos = mapping(pygame.mouse.get_pos())

            pygame.display.set_caption(str(self.clock.get_fps()))
            if self.start_game:
                if self.fight_flag:
                    # fight
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.run = False

                    cords_ = self.fight.render_fight(self.screen)
                    if cords_ is None:
                        self.fight_flag = False
                    else:
                        # send sms
                        sms = f'<fight {self.fight.magic_img_id} {cords_[0]} {cords_[1]}|' \
                              f'{self.opponent.persons.index(self.fight.enemy)} {self.fight.person_img_id} ' \
                              f'{int(self.fight.moves[0])} {int(self.fight.person_y)} {self.fight.person.hp},' \
                              f'{self.player.persons.index(self.fight.person)} {self.fight.enemy_img_id} ' \
                              f'{int(self.fight.moves[2])} {int(self.fight.enemy_y)} {self.fight.enemy.hp}>'
                        self.sock.send(sms.encode())

                        # recv sms
                        try:
                            self.data = self.sock.recv(1024).decode()
                            self.not_my_fight = False
                        except:
                            pass

                elif self.not_my_fight:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.run = False

                    # recv sms
                    try:
                        self.data = self.sock.recv(1024).decode()
                        if self.is_fight(self.data):
                            self.magic_data = self.find_fight_magic(self.data)
                            self.data = self.find_fight(self.data)
                            id_1, self.fight.person_img_id, self.fight.need_moves[
                                0], self.fight.person_y, self.fight.person.hp = self.data[1]

                            id_2, self.fight.enemy_img_id, self.fight.need_moves[
                                1], self.fight.enemy_y, self.fight.enemy.hp = self.data[0]

                            if self.fight.person.hp <= 0:
                                self.player.persons.remove(self.fight.person)
                        else:
                            self.not_my_fight = False
                            self.data = self.find_sms(self.data)
                    except:
                        pass
                    try:
                        self.fight.render_not_my_fight(self.screen, self.magic_data)
                    except:
                        print(self.fight)
                else:

                    if len(self.menu.choice_persons) == 0:
                        # events
                        self.events('main')
                    else:
                        self.events('place_persons')

                    if self.choice_person is None:
                        self.turn_menu = False
                        self.person_want_move = False
                        self.person_want_attack = False

                    if self.turn_phase == 'move':
                        self.unit_btn = None
                        self.move_btn = (20, 150, 200, 70)
                        self.attack_btn = None
                        self.wait_btn = (20, 220, 200, 70)
                    elif self.turn_phase == 'attack':
                        self.unit_btn = (20, 150, 200, 70)
                        self.move_btn = None
                        self.attack_btn = (20, 220, 200, 70)
                        self.wait_btn = (20, 290, 200, 70)

                    # send sms
                    sms = f'<{self.your_turn}|'
                    for person in self.player.persons:
                        sms += f'{person.name} {person.x} {person.y} {person.state}{person.move_to} ' \
                               f'{person.max_hp} {person.hp} {person.str} {person.mag} {person.skl} {person.lck} ' \
                               f'{person.def_} {person.res} {person.con} {person.movement} {person.speed} ' \
                               f'{person.hit} {person.dmg} {person.crt} {person.attack_speed} {person.avoid} ' \
                               f'{person.weapon.name} {person.lvl} {person.class_},'
                    sms += '>'
                    self.sock.send(sms.encode())

                    # recv sms
                    try:
                        data_ = self.sock.recv(1024).decode()
                        if data_[:5] == '<True' and self.turn_phase == 'move':
                            self.your_turn = True
                        elif data_[:6] == '<False':
                            self.your_turn = False
                        if self.your_turn != self.last_sms_to_move:
                            self.turn_phase = 'move'
                            self.choice_person = None
                            self.unit_btn = None
                            self.move_btn = (20, 150, 200, 70)
                            self.attack_btn = None
                            self.wait_btn = (20, 220, 200, 70)
                        self.last_sms_to_move = self.your_turn
                        if data_ == '<wait>':
                            pass
                        if self.is_fight(data_):
                            self.data = self.find_fight(data_)
                            self.not_my_fight = True
                            id_1, a_, b_, c_, d_ = self.data[1]
                            id_2, a_, b_, c_, d_ = self.data[0]
                            self.fight = Fight(self.player.persons[id_2],
                                               self.opponent.persons[id_1], self.fight_img, True)

                        else:
                            self.not_my_fight = False
                            self.data = self.find_sms(data_)
                            if len(self.data) != len(self.opponent.persons):
                                if [(int(j[1]) // TILE, int(j[2]) // TILE) for j in self.data] != \
                                        [person.pos for person in self.player.persons]:
                                    self.opponent.persons = [Person(int(j[1]), int(j[2]), j[0], None, j[20])
                                                             for j in self.data]
                    except:
                        print('no')
                    for j in range(len(self.data)):
                        if len(self.data[j]) > 10:
                            print(self.data)
                            self.opponent.persons[j].x = int(self.data[j][1])
                            self.opponent.persons[j].y = int(self.data[j][2])
                            self.opponent.persons[j].pos = (int(self.data[j][1]) // TILE,
                                                            int(self.data[j][2]) // TILE)
                            self.opponent.persons[j].max_hp = int(self.data[j][4])
                            self.opponent.persons[j].hp = int(self.data[j][5])
                            self.opponent.persons[j].str = int(self.data[j][6])
                            self.opponent.persons[j].mag = int(self.data[j][7])
                            self.opponent.persons[j].skl = int(self.data[j][8])
                            self.opponent.persons[j].lck = int(self.data[j][9])
                            self.opponent.persons[j].def_ = int(self.data[j][10])
                            self.opponent.persons[j].res = int(self.data[j][11])
                            self.opponent.persons[j].con = int(self.data[j][12])
                            self.opponent.persons[j].movement = int(self.data[j][13])
                            self.opponent.persons[j].speed = int(self.data[j][14])
                            self.opponent.persons[j].hit = int(self.data[j][15])
                            self.opponent.persons[j].dmg = int(self.data[j][16])
                            self.opponent.persons[j].crt = int(self.data[j][17])
                            self.opponent.persons[j].attack_speed = int(self.data[j][18])
                            self.opponent.persons[j].avoid = int(self.data[j][19])

                            w_last = self.opponent.persons[j].weapon.name
                            w_new = self.data[j][20]
                            if w_new != w_last:
                                self.opponent.persons[j].change_weapon(w_new)

                            self.opponent.persons[j].lvl = int(self.data[j][21])
                            self.opponent.persons[j].class_ = self.data[j][22]

                    # attack
                    for person in self.player.persons:
                        a_ = []
                        b_ = []
                        for enemy in self.opponent.persons:
                            if abs(person.pos[0] - enemy.pos[0]) + \
                                    abs(person.pos[1] - enemy.pos[1]) in person.weapon.range:
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
                    if self.not_my_fight:
                        pass
                    else:
                        self.render()
            else:
                self.events('menu')

                data_ = self.sock.recv(1024).decode()
                if data_[:5] == '<wait' and data_[:6] != '<wait>':
                    self.fight_img.upload_images(self.menu.all_names_persons[i] for i in self.menu.choice_persons)
                    data_ = self.find_persons_images(data_)
                    self.fight_img.upload_images(data_)
                    self.start_game = True
                    self.sms = '<ready>'
                elif data_[1:10].split(' ')[0] in self.menu.all_names_persons:
                    self.start_game = True
                self.sock.send(self.sms.encode())

                if not self.start_game:
                    self.menu.render(self.sms[:8] != '<my_pers')

            for person in self.player.persons + self.opponent.persons:
                print(person.name)
                print('hp ', person.hp)
                print('str ', person.str)
                print('mag ', person.mag)
                print('skl ', person.skl)
                print('speed ', person.speed)
                print('lck ', person.lck)
                print('def ', person.def_)
                print('res ', person.res)
                print('dmg ', person.dmg)
                print('attack_spped ', person.attack_speed)
                print('hit ', person.hit)
                print('avoid ', person.avoid)
                print('class ', person.class_)
                print('---------------------')

            pygame.display.update()


main = Main()

main.main_loop()
pygame.quit()
