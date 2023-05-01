import socket
import pygame

server_ip = '82.146.45.210'

main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
main_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
main_socket.bind((server_ip, 10000))
main_socket.setblocking(0)
main_socket.listen(5)

pygame.init()
clock = pygame.time.Clock()

FPS = 60
TILE = 80
tick = 0
is_fight = False
fight_person = ''
fight_sms = ''


class Person:
    def __init__(self, x, y, name, state, hp, armor, damage, critical):
        self.name = name
        self.pos = (x, y)
        self.state = state

        self.hp = hp
        self.armor = armor
        self.damage = damage
        self.critical = critical

    def get_big_pos(self):
        return (self.pos[0] * TILE, self.pos[1] * TILE)


class Player:
    def __init__(self, conn, addr):
        self.addr = addr
        self.conn = conn
        self.errors = 0
        self.persons = []
        self.is_fight = False
        self.ready = False


def find(s):
    first = None
    for i in range(len(s)):
        if s[i] == '<':
            first = i
        if s[i] == '>' and first is not None:
            end = i
            res = s[first + 1:end].split(',')
            res = [i.split(' ') for i in res if i != '']
            result = [[i[0], int(i[1]), int(i[2]), i[3], int(i[4]), int(i[5]), int(i[6]), int(i[7])] for i in res]
            return result
    return ''


players = []
run = True
while run:
    tick += 1
    clock.tick(FPS)

    if tick == 200:
        tick = 0
        # проверим, есть ли желающие войти в игру
        try:
            new_socket, addr = main_socket.accept()
            new_socket.setblocking(0)
            new_player = Player(new_socket, addr)
            players.append(new_player)
            print(f'Подключился игрок, игроков на сервере: {len(players)}')
        except:
            pass

    for player in players:
        try:
            data = player.conn.recv(1024).decode()
            if data[:6] == '<wait>':
                pass
            elif data[:7] == '<ready>':
                player.ready = True
            elif data[:6] == '<fight':
                player.is_fight = True
                fight_sms = data
            else:
                player.is_fight = False
                data = find(data)
                player.persons = [Person(i[1], i[2], i[0], i[3], i[4], i[5], i[6], i[7]) for i in data]
        except:
            pass

    for player in players:
        try:
            sms = '<wait>'
            if len(players) < 2:
                sms = '<wait>'
            else:
                if not players[0].ready or not players[1].ready:
                    sms = '<wait>'
                elif players[0].is_fight or players[1].is_fight:
                    if not player.is_fight:
                        sms = fight_sms
                else:
                    sms = '<'
                    for player_2 in players:
                        if player_2 != player:
                            for person in player_2.persons:
                                sms += f'{person.name} {person.pos[0]} {person.pos[1]} {person.state} ' \
                                       f'{person.hp} {person.armor} {person.damage} {person.critical},'
                    sms += '>'
            player.conn.send(sms.encode())
            player.errors = 0
        except:
            player.errors += 1
            if player.errors > 200:
                player.conn.close()
                players.remove(player)
                print(f'Отключился игрок, игроков на сервере: {len(players)}')
