import pygame
from person import Person
from player import Player
from settings import *
from dextr import *
import socket
from fight import Fight


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

        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('RPG')
        self.clock = pygame.time.Clock()

        # self.server_ip = '82.146.45.210'
        self.server_ip = 'localhost'
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.sock.connect((self.server_ip, 10000))

        self.bg = pygame.image.load('templates/map/map1.png')
        self.bg = pygame.transform.scale(self.bg, (1200, 800))

        self.mouse_pos = (0, 0)
        self.big_mouse_pos = (0, 0)

        self.players = [Player(), Player()]
        self.player = self.players[0]
        self.opponent = self.players[1]

        self.graph, self.cant = generate_graph('levels/lvl1.txt')
        self.can_move_to = []
        self.cords = []
        self.person_positions = []

        self.data = ''
        self.last_sms = ''
        self.can_move = True

        self.fight = False
        self.fight_person = None
        self.fight_enemy = None
        self.fight_tick = 0

        self.not_my_fight = False

    def find_sms(self, s):
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
            fight = Fight()

        # send sms
        sms = f'<fight {self.opponent.persons.index(self.fight_enemy)} {fight.person_img_id} ' \
              f'{int(fight.person_x)} {int(fight.person_y)} {self.fight_person.hp},' \
              f'{self.player.persons.index(self.fight_person)} {fight.enemy_img_id} ' \
              f'{int(fight.enemy_x)} {int(fight.enemy_y)} {self.fight_enemy.hp}>'
        print(sms)
        self.sock.send(sms.encode())

        # bg
        self.screen.blit(fight.fight_bg, (0, 0))

        # person
        if self.fight_tick <= 100:
            self.screen.blit(fight.person_stay_img, (200, 400))
            fight.person_img_id = 0
        elif self.fight_tick <= 245:
            img, cords_ = fight.mellee_person_attack()
            self.screen.blit(img, cords_)
            fight.person_img_id = 1 + fight.person_melee_attack_img.index(img)

        elif (self.fight_tick > 450) and (self.fight_tick < 455):
            fight.person_x = 190
            self.screen.blit(fight.person_stay_img, (190, 400))
            fight.person_img_id = 0
        elif (self.fight_tick > 455) and (self.fight_tick < 460):
            fight.person_x = 200
            self.screen.blit(fight.person_stay_img, (200, 400))
            fight.person_img_id = 0
            if self.fight_tick == 456:
                self.fight_person.hp -= self.fight_person.damage
        elif (self.fight_tick > 460) and (self.fight_tick < 465):
            fight.person_x = 190
            self.screen.blit(fight.person_stay_img, (190, 400))
            fight.person_img_id = 0

        else:
            self.screen.blit(fight.person_stay_img, (200, 400))

        # enemy
        if (self.fight_tick > 150) and (self.fight_tick < 155):
            fight.enemy_x = 710
            self.screen.blit(fight.enemy_stay_img, (710, 400))
            fight.enemy_img_id = 0
        elif (self.fight_tick > 155) and (self.fight_tick < 160):
            fight.enemy_x = 700
            self.screen.blit(fight.enemy_stay_img, (700, 400))
            fight.enemy_img_id = 0
            if self.fight_tick == 156:
                self.fight_enemy.hp -= self.fight_enemy.damage
        elif (self.fight_tick > 160) and (self.fight_tick < 165):
            fight.enemy_x = 710
            self.screen.blit(fight.enemy_stay_img, (710, 400))
            fight.enemy_img_id = 0

        elif self.fight_tick <= 400:
            self.screen.blit(fight.enemy_stay_img, (700, 400))
            fight.enemy_img_id = 0
        elif self.fight_tick <= 545:
            img, cords_ = fight.mellee_enemy_attack()
            self.screen.blit(img, cords_)
            fight.enemy_img_id = 1 + fight.enemy_melee_attack_img.index(img)
        else:
            self.screen.blit(fight.enemy_stay_img, (700, 400))
            fight.enemy_img_id = 0

        f1 = pygame.font.Font(None, 30)
        f2 = pygame.font.Font(None, 50)

        # name
        pygame.draw.rect(self.screen, BLUE, (0, 50, 150, 50))
        pygame.draw.rect(self.screen, RED, (1050, 50, 150, 50))
        name_person = 'Eliwood' if self.fight_person.name == 'eliwood(lord)' else self.fight_person.name
        name_enemy = 'Eliwood' if self.fight_enemy.name == 'eliwood(lord)' else self.fight_enemy.name
        text_name = f1.render(name_person, True, WHITE)
        self.screen.blit(text_name, (20, 65))
        text_name = f1.render(name_enemy, True, WHITE)
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

        text_arm = f2.render(str(self.fight_person.armor), True, WHITE)
        text_dmg = f2.render(str(self.fight_person.damage), True, WHITE)
        text_crt = f2.render(str(self.fight_person.critical), True, WHITE)
        self.screen.blit(f2.render('ARM', True, WHITE), (10, 605))
        self.screen.blit(f2.render('DMG', True, WHITE), (10, 634))
        self.screen.blit(f2.render('CRT', True, WHITE), (10, 662))
        self.screen.blit(text_arm, (100, 605))
        self.screen.blit(text_dmg, (100, 634))
        self.screen.blit(text_crt, (100, 662))

        text_arm = f2.render(str(self.fight_enemy.armor), True, WHITE)
        text_dmg = f2.render(str(self.fight_enemy.damage), True, WHITE)
        text_crt = f2.render(str(self.fight_enemy.critical), True, WHITE)
        self.screen.blit(f2.render('DMG', True, WHITE), (1010, 605))
        self.screen.blit(f2.render('DMG', True, WHITE), (1010, 634))
        self.screen.blit(f2.render('CRT', True, WHITE), (1010, 662))
        self.screen.blit(text_arm, (1100, 605))
        self.screen.blit(text_dmg, (1100, 634))
        self.screen.blit(text_crt, (1100, 662))

        # hp
        text_hp = f2.render(str(self.fight_person.hp), True, WHITE)
        self.screen.blit(text_hp, (100, 735))
        text_hp = f2.render(str(self.fight_enemy.hp), True, WHITE)
        self.screen.blit(text_hp, (900, 735))
        for i in range(0, int(self.fight_person.hp // 10)):
            pygame.draw.rect(self.screen, GREEN, (180 + i * 8, 730, 5, 40))
        for i in range(0, int(self.fight_enemy.hp // 10)):
            pygame.draw.rect(self.screen, GREEN, (980 + i * 8, 730, 5, 40))

        # end
        if self.fight_tick > 600:
            self.fight_tick = 0
            self.fight = False

    def render_not_my_fight(self):
        global fight
        self.fight_tick += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False

        if self.fight_tick == 1:
            fight = Fight()

        if self.not_my_fight:
            pass
        else:
            sms = '<'
            for person in self.player.persons:
                sms += f'{person.name} {person.x} {person.y} {person.state}{person.move_to},'
            sms += '>'
            if sms != self.last_sms:
                self.sock.send(sms.encode())
                self.last_sms = sms

        # recv sms
        try:
            self.data = self.sock.recv(1024).decode()
            if self.data[:6] == '<fight':
                self.data = main.find_fight(self.data)
                id_1, fight.person_img_id, fight.person_x, fight.person_y, self.fight_person.hp = self.data[1]
                fight.person_x = 200 + (700 - fight.person_x)

                id_2, fight.enemy_img_id, fight.enemy_x, fight.enemy_y, self.fight_enemy.hp = self.data[0]
                fight.enemy_x = 700 - (fight.enemy_x - 200)
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
        self.screen.blit(fight.person_stay_img if fight.person_img_id == 0
                         else fight.person_melee_attack_img[fight.person_img_id - 1],
                         (fight.person_x, fight.person_y))
        # enemy
        self.screen.blit(fight.enemy_stay_img if fight.enemy_img_id == 0
                         else fight.enemy_melee_attack_img[fight.enemy_img_id - 1],
                         (fight.enemy_x, fight.enemy_y))

        # characters person
        for i in range(0, int(self.fight_person.hp // 10)):
            pygame.draw.rect(self.screen, GREEN, (50 + i * 8, 730, 5, 40))

        # characters enemy
        for i in range(0, int(self.fight_enemy.hp // 10)):
            pygame.draw.rect(self.screen, GREEN, (1000 + i * 8, 730, 5, 40))

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
                for cord in self.cords:
                    pygame.draw.circle(self.screen, ORANGE,
                                       (cord[0] * TILE + TILE // 2, cord[1] * TILE + TILE // 2), TILE // 4)

        # persons
        for person in self.player.persons:
            # person move
            self.cords = person.move(self.cords)

            # person img
            person.choice_image(self.tick)

        for player in self.players:
            try:
                for i in range(len(player.persons)):
                    if player == self.opponent:

                        # opponent persons img
                        if self.data[i][3] == 'stay':
                            if self.tick % 120 < 60:
                                i_ = (self.tick % 60 // 10)
                            else:
                                i_ = 0
                            self.opponent.persons[i].img = self.opponent.persons[i].stay_images[i_]
                        elif self.data[i][3] == 'move_L':
                            self.opponent.persons[i].img = self.opponent.persons[i].move_images[self.tick % 40 // 20]
                        elif self.data[i][3] == 'move_R':
                            self.opponent.persons[i].img = self.opponent.persons[i].move_images[2 + self.tick % 40 // 20]
                        elif self.data[i][3] == 'move_D':
                            self.opponent.persons[i].img = self.opponent.persons[i].move_images[4 + self.tick % 40 // 20]
                        elif self.data[i][3] == 'move_U':
                            self.opponent.persons[i].img = self.opponent.persons[i].move_images[6 + self.tick % 40 // 20]

                    # person blit
                    self.screen.blit(player.persons[i].img,
                                     (player.persons[i].x - 45, player.persons[i].y - 60))
            except:
                pass

        # attack button
        for person in self.player.persons:
            if self.can_move:
                for i in person.attack_button:
                    pygame.draw.rect(self.screen, WHITE, i)

        # fps
        f1 = pygame.font.Font(None, 40)
        text = f1.render(str(self.clock.get_fps()), True, BLACK)
        self.screen.blit(text, (1150, 0))

    def menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_TAB:
                    self.start_game = True

        sms = '<wait>'
        self.sock.send(sms.encode())

        self.sock.recv(1024)

        self.screen.fill(GREY)
        pygame.display.update()

    def main_loop(self):
        while self.run:
            self.tick += 1
            self.clock.tick(FPS)
            if self.start_game:
                if self.fight:
                    main.render_fight()
                elif self.not_my_fight:
                    main.render_not_my_fight()
                else:
                    # events
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.run = False
                        if event.type == pygame.KEYUP:
                            if event.key == pygame.K_SPACE:
                                self.player.persons.append(Person(80, 80, 'eliwood(lord)'))
                            elif event.key == pygame.K_e:
                                self.can_move = True

                        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                            if self.player.choice_person is None:
                                if self.can_move:
                                    for person in self.player.persons:
                                        if self.mouse_pos == person.pos:
                                            self.player.choice_person = self.player.persons.index(person)
                                            self.person_positions = [person.pos for person in self.opponent.persons]
                                            self.can_move_to = main.get_can_move_to(person.pos, 3)
                                        else:
                                            for person in self.player.persons:
                                                i_ = 0
                                                for enemy in person.can_fight_with:
                                                    if in_box(self.big_mouse_pos, person.attack_button[i_]):
                                                        self.fight = True
                                                        self.fight_person = person
                                                        self.fight_enemy = person.can_fight_with[i_]
                                                        self.can_move = False
                                                    i_ += 1

                            elif self.player.choice_person is not None and self.mouse_pos in self.can_move_to:
                                self.player.persons[self.player.choice_person].want_move = self.mouse_pos
                                self.player.choice_person = None
                                self.can_move = False

                    # send sms
                    sms = '<'
                    for person in self.player.persons:
                        sms += f'{person.name} {person.x} {person.y} {person.state}{person.move_to} ' \
                               f'{person.hp} {person.armor} {person.damage} {person.critical},'
                    sms += '>'
                    self.sock.send(sms.encode())
                    self.last_sms = sms

                    # recv sms
                    try:
                        self.data = self.sock.recv(1024).decode()

                        if self.data[:6] == '<fight':
                            self.data = main.find_fight(self.data)
                            self.not_my_fight = True
                            id_1, a_, b_, c_, d_ = self.data[1]
                            id_2, a_, b_, c_, d_ = self.data[0]
                            self.fight_person = self.player.persons[id_2]
                            self.fight_enemy = self.opponent.persons[id_1]
                        else:
                            self.not_my_fight = False
                            self.data = main.find_sms(self.data)
                            if len(self.data) != len(self.opponent.persons):
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
                        print('Error')
                    self.mouse_pos = mapping(pygame.mouse.get_pos())
                    self.big_mouse_pos = pygame.mouse.get_pos()
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

                    if self.not_my_fight:
                        pass
                    else:
                        main.render()
                pygame.display.update()
            else:
                main.menu()


main = Main()

main.main_loop()
pygame.quit()
