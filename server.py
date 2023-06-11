import socket
import pygame
from random import randint

server_ip = '82.146.45.210'
server_ip = 'localhost'

main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
main_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
main_socket.bind((server_ip, 10000))
main_socket.setblocking(0)
main_socket.listen(5)

pygame.init()
clock = pygame.time.Clock()

FPS = 50
TILE = 80
tick = 0
is_fight = False
fight_person = ''
fight_sms = ''


class Player:
    def __init__(self, conn, addr):
        self.addr = addr
        self.conn = conn
        self.errors = 0
        self.is_fight = False
        self.ready = False
        self.person_names = []
        self.can_move = False
        self.last_sms_move = None
        self.sms = ''


def find(s):
    first = None
    if s[:5] == '<True':
        can_move = True
    elif s[:5] == '<None':
        can_move = None
    else:
        can_move = False
    for i in range(len(s)):
        if s[i] == '|':
            first = i
        if s[i] == '>' and first is not None:
            end = i
            res = s[first + 1:end].split(',')
            res = [i.split(' ') for i in res if i != '']
            result = [[i[0], int(i[1]), int(i[2]), i[3], int(i[4]), int(i[5]), int(i[6]), int(i[7]), i[8], int(i[9])]
                      for i in res]
            return can_move, result
    return ''


def find_player_persons(s):
    first = None
    for i in range(len(s)):
        if s[i] == '|':
            first = i
        if s[i] == '>' and first is not None:
            end = i
            res = s[first + 1:end - 1].split(',')
            return res
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
            if len(players) == 2:
                players[randint(0, 1)].can_move = True
        except:
            pass

    for player in players:
        try:
            data = player.conn.recv(1024).decode()
            if data[:6] == '<wait>':
                pass
            elif data[:8] == '<my_pers':
                player.person_names = find_player_persons(data)
            elif data[:6] == '<ready':
                player.ready = True
            elif data[:6] == '<fight':
                player.is_fight = True
                fight_sms = data
                message = data.split(' ')
            else:
                player.is_fight = False
                data = data.split('|')
                if data[0] == '<True':
                    a = True
                elif data[0] == '<None':
                    a = None
                else:
                    a = False

                if a is None:
                    player.last_sms_move = player.can_move
                elif player.last_sms_move != a and player.can_move:
                    player.can_move = a
                    player.last_sms_move = a
                    for player_2 in players:
                        if player_2 != player:
                            player_2.can_move = not a
                            print(players.index(player), 'change', player.can_move, player_2.can_move)
                player.sms = data[1][:-1]
        except:
            pass

    print('-------')
    for player in players:
        second_player = None
        for player_2 in players:
            if player_2 != player:
                second_player = player_2
        try:
            sms = '<wait>'
            if len(players) < 2:
                sms = '<wait>'
            else:
                if player.person_names == [] or second_player.person_names == []:
                    pass
                elif (player.person_names != [] and second_player.person_names != []) and not player.ready:
                    sms = f'<wait |'
                    for name in second_player.person_names:
                        sms += name + ' '
                    sms += '>'
                elif players[0].is_fight or players[1].is_fight:
                    if not player.is_fight:
                        sms = fight_sms
                else:
                    sms = f'<{player.can_move}|'
                    for player_2 in players:
                        if player_2 != player:
                            sms += player_2.sms
                    sms += '>'
            player.conn.send(sms.encode())
            print(sms)
            player.errors = 0
        except:
            player.errors += 1
            if player.errors > 200:
                player.conn.close()
                players.remove(player)
                print(f'Отключился игрок, игроков на сервере: {len(players)}')