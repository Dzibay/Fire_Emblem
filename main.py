import pygame
from person import Person
from player import Player
from settings import *
from dextr import *
import socket


def mapping(pos):
    return (pos[0] // TILE, pos[1] // TILE)


class Main:
    def __init__(self):
        self.start_game = False
        self.run = True
        self.tick = 0

        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('RPG')
        self.clock = pygame.time.Clock()

        self.server_ip = 'localhost'
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.sock.connect((self.server_ip, 10000))

        self.bg = pygame.image.load('templates/map/map1.png')
        self.bg = pygame.transform.scale(self.bg, (1200, 800))

        self.mouse_pos = (0, 0)

        self.players = [Player(), Player()]
        self.player = self.players[0]
        self.opponent = self.players[1]

        self.cant = []
        self.graph = None
        self.cords = []
        self.person_positions = []

        self.data = ''
        self.last_sms = ''
        self.can_move = True

    def find_sms(self, s):
        first = None
        for i in range(len(s)):
            if s[i] == '<':
                first = i
            if s[i] == '>' and first is not None:
                end = i
                res = s[first + 1:end].split(',')
                res = [i.split(' ') for i in res if len(i) > 0]
                result = [(i[0], int(i[1]), int(i[2]), i[3]) for i in res]
                return result
        return None

    def render(self):
        # bg
        self.screen.blit(self.bg, (0, 0))
        for x in range(0, WIDTH, TILE):
            for y in range(0, HEIGHT, TILE):
                pygame.draw.rect(self.screen, WHITE, (x, y, TILE, TILE), 1)

        # mouse
        pygame.draw.rect(self.screen, BLACK, (self.mouse_pos[0] * TILE, self.mouse_pos[1] * TILE, TILE, TILE), 1)
        if self.player.choice_person is not None:
            p_ = self.player.persons[self.player.choice_person]
            pygame.draw.rect(self.screen, ORANGE, (p_.get_big_pos()[0], p_.get_big_pos()[1], TILE, TILE), 3)

            if self.mouse_pos not in self.person_positions:
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
            for i in range(len(player.persons)):
                if player == self.opponent:

                    # opponent persons img
                    if self.data[i][3] == 'stay':
                        if self.tick % 120 < 60:
                            i_ = (self.tick % 60 // 10)
                        else:
                            i_ = 0
                        self.opponent.persons[i].img = self.opponent.persons[i].stay_images[i_]

                # person blit
                self.screen.blit(player.persons[i].img,
                                 (player.persons[i].x - 45, player.persons[i].y - 60))

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
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.run = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.player.persons.append(Person(80, 80, 'eliwood(lord)'))
                        elif event.key == pygame.K_e:
                            self.can_move = True

                    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        if self.player.choice_person is None:
                            if self.can_move:
                                for person in self.player.persons:
                                    if self.mouse_pos == person.pos:
                                        if self.player.choice_person is None:
                                            self.player.choice_person = self.player.persons.index(person)
                                            self.person_positions = [person.pos for person in self.player.persons
                                                                     if person != self.player.persons[self.player.choice_person]]
                                            self.graph, self.cant = generate_graph('levels/lvl1.txt', self.person_positions)
                                        else:
                                            self.player.choice_person = None
                        else:
                            if self.mouse_pos not in self.cant and self.mouse_pos not in self.person_positions:
                                self.player.persons[self.player.choice_person].want_move = self.mouse_pos
                                self.player.choice_person = None
                                self.can_move = False

                # send sms
                sms = '<'
                for person in self.player.persons:
                    sms += f'{person.name} {person.x} {person.y} {person.state}{person.move_to},'
                sms += '>'
                if sms != self.last_sms:
                    self.sock.send(sms.encode())
                    self.last_sms = sms
                print(sms)

                # recv sms
                try:
                    self.data = self.sock.recv(1024).decode()
                    self.data = main.find_sms(self.data)
                    if len(self.data) != len(self.opponent.persons):
                        self.opponent.persons = [Person(j[1], j[2], j[0]) for j in self.data]
                    for j in range(len(self.data)):
                        self.opponent.persons[j].x = self.data[j][1]
                        self.opponent.persons[j].y = self.data[j][2]
                except:
                    pass

                self.mouse_pos = mapping(pygame.mouse.get_pos())

                main.render()
                pygame.display.update()
            else:
                main.menu()


main = Main()

main.main_loop()
pygame.quit()
