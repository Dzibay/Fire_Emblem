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

        self.players = [Player()]
        self.player = self.players[0]

        self.cant = []
        self.graph = None
        self.person_positions = []

        self.last_sms = ''
        self.last_data = ''
        self.can_move = True

    def find_sms(self, s):
        first = None
        for i in range(len(s)):
            if s[i] == '<':
                first = i
            if s[i] == '>' and first is not None:
                end = i
                res = s[first + 1:end].split('|')
                res = [i.split(',') for i in res if len(i) > 0]
                res = [[i.split(' ') for i in j if len(i) > 0] for j in res]
                result = [[(i[0], int(i[1]), int(i[2])) for i in j] for j in res]
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
                cords = get_cords(self.graph, p_.pos, self.mouse_pos)
                for cord in cords:
                    pygame.draw.circle(self.screen, ORANGE,
                                       (cord[0] * TILE + TILE // 2, cord[1] * TILE + TILE // 2), TILE // 4)

        # persons
        for person in self.player.persons:
            if self.tick % 240 < 120:
                i_ = (self.tick % 120 // 20)
            else:
                i_ = 0
            self.screen.blit(person.state_images[i_], (person.get_big_pos()[0] - 10, person.get_big_pos()[1] - 10))

        # fps
        f1 = pygame.font.Font(None, 40)
        text = f1.render(str(self.clock.get_fps()), True, BLACK)
        self.screen.blit(text, (1150, 0))

    def main_loop(self):
        run = True
        while run:
            self.tick += 1
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
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
                sms += f'{person.name} {person.x} {person.y},'
            sms += '>'
            if sms != self.last_sms:
                self.sock.send(sms.encode())
                self.last_sms = sms

            # recv sms
            data = self.sock.recv(1024).decode()
            data = main.find_sms(data)
            if data != self.last_data:
                if len(data) != len(self.players):
                    self.players = [Player() for i in data]
                for i in range(len(data)):
                    if len(data[i]) != len(self.players[i].persons):
                        self.players[i].persons = [Person(j[1], j[2], j[0]) for j in data[i]]
                    for j in range(len(data[i])):
                        self.players[i].persons[j].name = data[i][j][0]
                        self.players[i].persons[j].x = data[i][j][1]
                        self.players[i].persons[j].x = data[i][j][2]

            self.mouse_pos = mapping(pygame.mouse.get_pos())

            # person move
            for player in self.players:
                for person in player.persons:
                    print(person.want_move)
                    person.move()

            main.render()
            pygame.display.update()


main = Main()

main.main_loop()
pygame.quit()
