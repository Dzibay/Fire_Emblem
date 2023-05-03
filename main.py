import pygame
from person import Person
from player import Player
from settings import *
from dextr import *
import socket
from fight import Fight, Fight_images

import time


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
        self.tick = 0

        # pygame
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('RPG')
        self.clock = pygame.time.Clock()

        # socket
        # self.server_ip = '82.146.45.210'
        self.server_ip = 'localhost'
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.sock.connect((self.server_ip, 10000))

        # bg
        self.bg = pygame.image.load('templates/map/map1.png')
        self.bg = pygame.transform.scale(self.bg, (1200, 800))

        # mouse
        self.mouse_pos = (0, 0)
        self.big_mouse_pos = (0, 0)

        # players
        self.players = [Player(), Player()]
        self.player = self.players[0]
        self.opponent = self.players[1]

        # move
        self.graph, self.cant = generate_graph('levels/lvl1.txt')
        self.can_move_to = []
        self.cords = []
        self.person_positions = []

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
        self.last_sms = ''
        self.can_move = True

        # fight
        self.fight_img = None
        self.fight = False
        self.not_my_fight = False
        self.fight_person = None
        self.fight_enemy = None
        self.fight_tick = 0

        # menu
        self.sms = '<wait>'
        self.menu_tick = 0
        self.menu_btn_cords = (450, 550, 300, 50)
        self.menu_person_choice_cords = [(i, j, 100, 100) for j in range(50, 530, 120) for i in range(250, 950, 120)]
        self.names_choice_persons = ['roy', 'roy', 'lyn']
        self.menu_person_img = [
            pygame.image.load(f'templates/persons/{i}/person/map_idle.png').subsurface((0, 0, 48, 48))
            for i in self.names_choice_persons]
        for i in range(len(self.menu_person_img)):
            self.menu_person_img[i] = pygame.transform.scale(self.menu_person_img[i], (200, 200))
        self.menu_choice_persons = []

        # placing persons
        self.placing_persons_window = False
        self.placing_choice_person = None
        self.placing_persons_pos = [(20, 660), (120, 660), (220, 660), (320, 660), (420, 660), (520, 660)]

        # fonts
        self.f1 = pygame.font.Font(None, 30)
        self.f2 = pygame.font.Font(None, 50)

    @staticmethod
    def find_sms(s):
        first = None
        for i in range(len(s)):
            if s[i] == '<':
                first = i
            if s[i] == '>' and first is not None:
                end = i
                res = s[first + 1:end].split(',')
                res = [i.split(' ') for i in res if len(i) > 0]
                result = [(i[0], int(i[1]), int(i[2]), i[3], int(i[4]), int(i[5]), int(i[6]), int(i[7])) for i in res]
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
    def find_fight(s):
        first = None
        for i in range(len(s)):
            if s[i] == '<':
                first = i
            if s[i] == '>' and first is not None:
                end = i
                res = s[first + 1:end][6:].split(',')
                res = [[int(i) for i in j.split(' ')] for j in res]
                return res
        return ''

    def get_can_move_to(self, pos, l):
        res = [(x, y)
               for x in range(pos[0] - l, pos[0] + l + 1) if x >= 0
               for y in range(pos[1] - l, pos[1] + l + 1) if y >= 0]
        result = []
        for i in res:
            cords = get_cords(self.graph, pos, i)
            if (i not in self.cant) and \
                    (i not in self.person_positions) and \
                    (len(cords) <= l + 1):
                result.append(i)
        return result

    def render_persons_characters_for_fight(self):
        # name
        pygame.draw.rect(self.screen, BLUE, (0, 50, 150, 50))
        pygame.draw.rect(self.screen, RED, (1050, 50, 150, 50))
        text_name = self.f1.render(self.fight_person.name, True, WHITE)
        self.screen.blit(text_name, (20, 65))
        text_name = self.f1.render(self.fight_enemy.name, True, WHITE)
        self.screen.blit(text_name, (1070, 65))

        # characters persons
        pygame.draw.rect(self.screen, BLUE, (0, 700, 600, 100))
        pygame.draw.rect(self.screen, RED, (600, 700, 600, 100))
        pygame.draw.rect(self.screen, ORANGE, (0, 700, 600, 100), 5)
        pygame.draw.rect(self.screen, ORANGE, (600, 700, 600, 100), 5)

        pygame.draw.rect(self.screen, (100, 65, 0), (0, 600, 200, 100))
        pygame.draw.rect(self.screen, BLUE, (0, 617.5, 200, 10))
        pygame.draw.rect(self.screen, BLUE, (0, 645, 200, 10))
        pygame.draw.rect(self.screen, BLUE, (0, 672.5, 200, 10))
        pygame.draw.rect(self.screen, ORANGE, (0, 600, 200, 100), 5)

        pygame.draw.rect(self.screen, (100, 65, 0), (1000, 600, 200, 100))
        pygame.draw.rect(self.screen, RED, (1000, 617.5, 200, 10))
        pygame.draw.rect(self.screen, RED, (1000, 645, 200, 10))
        pygame.draw.rect(self.screen, RED, (1000, 672.5, 200, 10))
        pygame.draw.rect(self.screen, ORANGE, (1000, 600, 200, 100), 5)

        text_arm = self.f2.render(str(self.fight_person.armor), True, WHITE)
        text_dmg = self.f2.render(str(self.fight_person.damage), True, WHITE)
        text_crt = self.f2.render(str(self.fight_person.critical), True, WHITE)
        self.screen.blit(self.f2.render('ARM', True, WHITE), (10, 605))
        self.screen.blit(self.f2.render('DMG', True, WHITE), (10, 634))
        self.screen.blit(self.f2.render('CRT', True, WHITE), (10, 662))
        self.screen.blit(text_arm, (100, 605))
        self.screen.blit(text_dmg, (100, 634))
        self.screen.blit(text_crt, (100, 662))

        text_arm = self.f2.render(str(self.fight_enemy.armor), True, WHITE)
        text_dmg = self.f2.render(str(self.fight_enemy.damage), True, WHITE)
        text_crt = self.f2.render(str(self.fight_enemy.critical), True, WHITE)
        self.screen.blit(self.f2.render('DMG', True, WHITE), (1010, 605))
        self.screen.blit(self.f2.render('DMG', True, WHITE), (1010, 634))
        self.screen.blit(self.f2.render('CRT', True, WHITE), (1010, 662))
        self.screen.blit(text_arm, (1100, 605))
        self.screen.blit(text_dmg, (1100, 634))
        self.screen.blit(text_crt, (1100, 662))

        # hp
        text_hp = self.f2.render(str(self.fight_person.hp), True, WHITE)
        self.screen.blit(text_hp, (100, 735))
        text_hp = self.f2.render(str(self.fight_enemy.hp), True, WHITE)
        self.screen.blit(text_hp, (900, 735))
        for i in range(0, int(self.fight_person.hp // 10)):
            pygame.draw.rect(self.screen, GREEN, (180 + i * 8, 730, 5, 40))
        for i in range(0, int(self.fight_enemy.hp // 10)):
            pygame.draw.rect(self.screen, GREEN, (980 + i * 8, 730, 5, 40))

    def render_fight(self):
        global fight
        self.fight_tick += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.fight = False
                    self.fight_tick = 0

        if self.fight_tick == 1:
            fight = Fight(self.fight_person.name, self.fight_enemy.name,
                          self.fight_img, self.fight_person.critical, self.fight_enemy.critical)

        # send sms
        sms = f'<fight {self.opponent.persons.index(self.fight_enemy)} {fight.person_img_id} ' \
              f'{int(fight.person_x)} {int(fight.person_y)} {self.fight_person.hp},' \
              f'{self.player.persons.index(self.fight_person)} {fight.enemy_img_id} ' \
              f'{int(fight.enemy_x)} {int(fight.enemy_y)} {self.fight_enemy.hp}>'
        self.sock.send(sms.encode())

        # recv sms
        try:
            self.data = self.sock.recv(1024).decode()
            self.not_my_fight = False
        except:
            pass

        # bg
        self.screen.blit(fight.fight_bg, (0, 0))

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
        # person
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
                    k_ = 2 if fight.moves[2] else 1
                    self.fight_person.hp -= self.fight_enemy.damage * k_

            if not fight.moves[1]:
                if (self.fight_tick > enemy_dmg_tick) and (self.fight_tick < enemy_dmg_tick + 5):
                    fight.enemy_x += 10
                elif (self.fight_tick > enemy_dmg_tick + 5) and (self.fight_tick < enemy_dmg_tick + 10):
                    fight.enemy_x -= 10
                if self.fight_tick == enemy_dmg_tick + 6:
                    k_ = 2 if fight.moves[0] else 1
                    self.fight_enemy.hp -= self.fight_person.damage * k_
        self.screen.blit(img, (fight.person_x, fight.person_y))
        self.screen.blit(img_, (fight.enemy_x, fight.enemy_y))
        fight.person_img_id = fight.all_person_img.index(img)
        fight.enemy_img_id = fight.all_enemy_img.index(img_)

        # name
        pygame.draw.rect(self.screen, BLUE, (0, 50, 150, 50))
        pygame.draw.rect(self.screen, RED, (1050, 50, 150, 50))
        text_name = self.f1.render(self.fight_person.name, True, WHITE)
        self.screen.blit(text_name, (20, 65))
        text_name = self.f1.render(self.fight_enemy.name, True, WHITE)
        self.screen.blit(text_name, (1070, 65))

        # characters persons
        main.render_persons_characters_for_fight()

        # end
        if self.fight_tick > fight_end:
            self.fight_tick = 0
            self.fight = False

    def render_not_my_fight(self):
        global fight
        self.fight_tick += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False

        if self.fight_tick == 1:
            fight = Fight(self.fight_person.name, self.fight_enemy.name, self.fight_img)

        # recv sms
        try:
            self.data = self.sock.recv(1024).decode()
            if main.is_fight(self.data):
                self.data = main.find_fight(self.data)
                id_1, fight.person_img_id, fight.enemy_x, fight.person_y, self.fight_person.hp = self.data[1]
                id_2, fight.enemy_img_id, fight.person_x, fight.enemy_y, self.fight_enemy.hp = self.data[0]
            else:
                self.not_my_fight = False
                self.data = main.find_sms(self.data)
                if len(self.data) != len(self.opponent.persons):
                    self.opponent.persons = [Person(j[1], j[2], j[0], 'R') for j in self.data]
                for j in range(len(self.data)):
                    self.opponent.persons[j].x = self.data[j][1]
                    self.opponent.persons[j].y = self.data[j][2]
        except:
            pass

        self.screen.blit(fight.fight_bg, (0, 0))
        # person
        self.screen.blit(fight.all_person_img[fight.person_img_id], (fight.person_x, fight.person_y))
        # enemy
        self.screen.blit(fight.all_enemy_img[fight.enemy_img_id], (fight.enemy_x, fight.enemy_y))

        # characters persons
        main.render_persons_characters_for_fight()

    def render(self):
        # bg
        self.screen.blit(self.bg, (0, 0))
        for x in range(0, WIDTH, TILE):
            for y in range(0, HEIGHT, TILE):
                pygame.draw.rect(self.screen, WHITE, (x, y, TILE, TILE), 1)

        # mouse
        pygame.draw.rect(self.screen, BLACK, (self.mouse_pos[0] * TILE, self.mouse_pos[1] * TILE, TILE, TILE), 1)
        if self.player.choice_person is not None:

            # choice person
            p_ = self.player.persons[self.player.choice_person]
            pygame.draw.rect(self.screen, ORANGE, (p_.get_big_pos()[0], p_.get_big_pos()[1], TILE, TILE), 3)

            # can move to
            for i in self.can_move_to:
                rect = pygame.Surface((TILE, TILE))
                rect.fill(BLUE)
                rect.set_alpha(100)
                self.screen.blit(rect, (i[0] * TILE, i[1] * TILE))

            # orange circles
            if self.mouse_pos in self.can_move_to:
                self.cords = get_cords(self.graph, p_.pos, self.mouse_pos)
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
                                (self.cords[i + 1][0] < self.cords[i][0] and self.cords[i][1] < self.cords[i - 1][1]):
                            img = 'r-d'
                        elif (self.cords[i - 1][0] < self.cords[i][0] and self.cords[i][1] > self.cords[i + 1][1]) or \
                                (self.cords[i + 1][0] < self.cords[i][0] and self.cords[i][1] > self.cords[i - 1][1]):
                            img = 'r-u'
                        elif (self.cords[i - 1][0] > self.cords[i][0] and self.cords[i][1] < self.cords[i + 1][1]) or \
                                (self.cords[i + 1][0] > self.cords[i][0] and self.cords[i][1] < self.cords[i - 1][1]):
                            img = 'u-r'
                        elif (self.cords[i - 1][0] > self.cords[i][0] and self.cords[i][1] > self.cords[i + 1][1]) or \
                                (self.cords[i + 1][0] > self.cords[i][0] and self.cords[i][1] > self.cords[i - 1][1]):
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
                        self.screen.blit(self.pointer[img], (self.cords[i][0] * TILE, self.cords[i][1] * TILE))

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
                self.screen.blit(player.persons[i].img,
                                 (player.persons[i].x - 88, player.persons[i].y - 100))

        if len(self.menu_choice_persons) == 0:
            # attack button
            try:
                for person in self.player.persons:
                    if self.can_move:
                        for i in person.attack_button:
                            pygame.draw.rect(self.screen, WHITE, i)
            except:
                pass

            # see person info
            for person in self.player.persons + self.opponent.persons:

                # rect
                if self.mouse_pos == person.pos:
                    if person in self.player.persons:
                        pygame.draw.rect(self.screen, BLUE, (975, 50, 200, 300))
                    else:
                        pygame.draw.rect(self.screen, RED, (975, 50, 200, 300))

                    # name
                    text_name = self.f2.render(person.name, True, WHITE)
                    self.screen.blit(text_name, (990, 60))

                    # hp
                    text_hp = self.f2.render(str(person.hp), True, WHITE)
                    self.screen.blit(text_hp, (990, 100))
                    for i in range(person.hp // 10):
                        pygame.draw.rect(self.screen, GREEN, (1055 + i * 10, 105, 5, 20))

                    # characters
                    text_armor = self.f2.render('ARM', True, WHITE)
                    text_arm = self.f2.render(str(person.armor), True, WHITE)
                    text_damage = self.f2.render('DMG', True, WHITE)
                    text_dmg = self.f2.render(str(person.damage), True, WHITE)
                    text_critical = self.f2.render('CRT', True, WHITE)
                    text_crt = self.f2.render(str(person.critical), True, WHITE)
                    self.screen.blit(text_armor, (1000, 150))
                    self.screen.blit(text_damage, (1000, 200))
                    self.screen.blit(text_critical, (1000, 250))
                    self.screen.blit(text_arm, (1100, 150))
                    self.screen.blit(text_dmg, (1100, 200))
                    self.screen.blit(text_crt, (1100, 250))

        # person placing window
        if self.placing_persons_window:
            pygame.draw.rect(self.screen, BLUE, (0, 650, WIDTH, 150))
            for i in self.menu_choice_persons:
                img = self.menu_person_img[i]
                self.screen.blit(img, (self.placing_persons_pos[i][0] - 50, self.placing_persons_pos[i][1] - 50))
            if self.placing_choice_person is not None:
                pos_ = self.placing_persons_pos[self.placing_choice_person]
                pygame.draw.rect(self.screen, WHITE, (pos_[0], pos_[1], 100, 100), 2)

        # fps
        text_fps = self.f1.render(str(self.clock.get_fps()), True, BLACK)
        self.screen.blit(text_fps, (1150, 0))

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
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.placing_persons_window:
                    for i in self.menu_choice_persons:
                        if in_box(self.big_mouse_pos,
                                  (self.placing_persons_pos[i][0], self.placing_persons_pos[i][1], 100, 100)):
                            if self.placing_choice_person != i:
                                self.placing_choice_person = i
                            else:
                                self.placing_choice_person = None
                else:
                    if self.placing_choice_person is not None:
                        self.player.persons.append(Person(self.mouse_pos[0] * TILE,
                                                          self.mouse_pos[1] * TILE,
                                                          self.names_choice_persons[self.placing_choice_person]))
                        self.menu_choice_persons.remove(self.placing_choice_person)
                        self.placing_choice_person = None

        sms = '<'
        for person in self.player.persons:
            sms += f'{person.name} {person.x} {person.y} {person.state}{person.move_to} ' \
                   f'{person.hp} {person.armor} {person.damage} {person.critical},'
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
                    self.opponent.persons = [Person(j[1], j[2], j[0], 'R') for j in self.data]

            for j in range(len(self.data)):
                self.opponent.persons[j].x = self.data[j][1]
                self.opponent.persons[j].y = self.data[j][2]
                self.opponent.persons[j].pos = (self.data[j][1] // TILE,
                                                self.data[j][2] // TILE)
                self.opponent.persons[j].hp = self.data[j][4]
                self.opponent.persons[j].armor = self.data[j][5]
                self.opponent.persons[j].damage = self.data[j][6]
                self.opponent.persons[j].critical = self.data[j][7]

        except:
            pass

    def menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            elif self.sms != '<ready>':
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if in_box(self.big_mouse_pos, self.menu_btn_cords):
                        self.sms = '<ready>'
                        self.menu_choice_persons = [self.menu_person_choice_cords.index(j) for j in
                                                    self.menu_choice_persons]
                        self.menu_choice_persons = [i for i in self.menu_choice_persons if
                                                    i < len(self.menu_person_img)]
                        self.placing_persons_window = True
                    else:
                        for i in self.menu_person_choice_cords:
                            if in_box(self.big_mouse_pos, i):
                                if i in self.menu_choice_persons:
                                    self.menu_choice_persons.remove(i)
                                else:
                                    self.menu_choice_persons.append(i)

        self.sock.send(self.sms.encode())

        data_ = self.sock.recv(1024).decode()
        if data_[:6] != '<wait>':
            self.start_game = True
            self.fight_img = Fight_images(['roy', 'lyn'])

        # draw
        self.screen.fill(GREY)
        if self.sms != '<ready>':
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
                                if event.key == pygame.K_SPACE:
                                    self.player.persons.append(Person(80, 80, 'eliwood(lord)'))
                                elif event.key == pygame.K_e:
                                    self.can_move = True
                                elif event.key == pygame.K_o:
                                    for person in self.player.persons:
                                        person.critical = 100
                                elif event.key == pygame.K_l:
                                    for person in self.player.persons:
                                        person.critical = 15

                            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                                if self.player.choice_person is None:
                                    if self.can_move:
                                        # choice person
                                        for person in self.player.persons:
                                            if self.mouse_pos == person.pos:
                                                self.player.choice_person = self.player.persons.index(person)
                                                self.person_positions = [person.pos for person in self.opponent.persons]
                                                self.can_move_to = main.get_can_move_to(person.pos, 3)
                                            else:
                                                # attack
                                                for person in self.player.persons:
                                                    i_ = 0
                                                    for enemy in person.can_fight_with:
                                                        if in_box(self.big_mouse_pos, person.attack_button[i_]):
                                                            self.fight_tick = 0
                                                            self.fight = True
                                                            self.fight_person = person
                                                            self.fight_enemy = person.can_fight_with[i_]
                                                            self.can_move = False
                                                            break
                                                        i_ += 1
                                # move
                                elif self.player.choice_person is not None and self.mouse_pos in self.can_move_to:
                                    if self.mouse_pos == self.player.persons[self.player.choice_person].pos:
                                        pass
                                    else:
                                        self.player.persons[self.player.choice_person].want_move = self.mouse_pos
                                        self.can_move = False
                                    self.player.choice_person = None

                        # send sms
                        sms = '<'
                        for person in self.player.persons:
                            sms += f'{person.name} {person.x} {person.y} {person.state}{person.move_to} ' \
                                   f'{person.hp} {person.armor} {person.damage} {person.critical},'
                        sms += '>'
                        self.sock.send(sms.encode())

                        # recv sms
                        try:
                            data_ = self.sock.recv(1024).decode()
                            if data_ == '<wait>':
                                self.start_game = False
                            if main.is_fight(data_):
                                self.data = main.find_fight(data_)
                                self.not_my_fight = True
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
                                        self.opponent.persons = [Person(j[1], j[2], j[0], 'R') for j in self.data]

                                for j in range(len(self.data)):
                                    self.opponent.persons[j].x = self.data[j][1]
                                    self.opponent.persons[j].y = self.data[j][2]
                                    self.opponent.persons[j].pos = (self.data[j][1] // TILE,
                                                                    self.data[j][2] // TILE)
                                    self.opponent.persons[j].hp = self.data[j][4]
                                    self.opponent.persons[j].armor = self.data[j][5]
                                    self.opponent.persons[j].damage = self.data[j][6]
                                    self.opponent.persons[j].critical = self.data[j][7]

                        except:
                            pass

                        # attack
                        for person in self.player.persons:
                            a_ = []
                            b_ = []
                            for enemy in self.opponent.persons:

                                if abs(person.pos[0] - enemy.pos[0]) <= 1 and abs(person.pos[1] - enemy.pos[1]) <= 1:
                                    a_.append(enemy)
                                    b_.append((enemy.pos[0] * TILE + TILE,
                                               enemy.pos[1] * TILE - (TILE / 2),
                                               100, 30))
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
