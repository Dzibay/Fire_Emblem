from collections import deque
from functools import lru_cache

import pygame


def bfs(graph, start, goal):
    queque = deque([start])
    visited = {start: None}

    while queque:
        cur_node = queque.popleft()
        if cur_node == goal:
            break

        next_nodes = graph[cur_node]
        for next_node in next_nodes:
            if next_node not in visited:
                queque.append(next_node)
                visited[next_node] = cur_node
    try:
        cur = goal
        a = [cur]
        while cur != start:
            cur = visited[cur]
            a.append(cur)
    except:
        a = []
    return a


@lru_cache
def generate_graph(file):
    not_zero = []
    lvl = open(file, 'r').readlines()
    lvl = [i.replace('\n', '') for i in lvl]
    matrix = [[int(i) for i in j] for j in lvl]
    cords = {(j, i): [] for i in range(len(matrix)) for j in range(len(matrix[0]))}
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] != 0:
                cords[(j, i)] = None
                not_zero.append((j, i))
    for cord in cords:
        if cord not in not_zero:
            cords_ = []
            if cord[0] != 0 and cords[(cord[0] - 1, cord[1])] is not None:
                cords_.append((cord[0] - 1, cord[1]))
            if cord[0] != 15 and cords[(cord[0] + 1, cord[1])] is not None:
                cords_.append((cord[0] + 1, cord[1]))
            if cord[1] != 0 and cords[(cord[0], cord[1] - 1)] is not None:
                cords_.append((cord[0], cord[1] - 1))
            if cord[1] != 19 and cords[(cord[0], cord[1] + 1)] is not None:
                cords_.append((cord[0], cord[1] + 1))
            cords[cord] = cords_

    return cords, not_zero


def get_cords(graph, start, goal):
    cords = bfs(graph, start, goal)
    return cords


def read(file, script=False):
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
                elif i[:9] == 'start_hit':
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
            if i[0][10:15] == 'under':
                result[len(result) - 1].append([int(j) for j in i[1:]])
            else:
                result.append([[int(j) for j in i[1:]]])
        return result


def test():
    pygame.init()
    pers = 'eliwood'
    weapon = 'bow'
    choice = 'critical'
    screen = pygame.display.set_mode((1000, 800))
    clock = pygame.time.Clock()
    index = read(open(f'templates/persons/{pers}/{weapon}/Index.txt').readlines())
    script = read(open(f'templates/persons/{pers}/{weapon}/Script.txt').readlines(), True)
    imgs = [[pygame.transform.flip(pygame.transform.scale(pygame.image.load(f'templates/persons/{pers}/{weapon}/attack.png').
            subsurface((i[0], i[1], i[2], i[3])), (i[2] * 5, i[3] * 5)), True, False) for i in j] for j in index]
    print(index)
    print(script)
    print(imgs)
    cadr = 0
    cadr_tick = 0
    script_navigator = 0
    attack = False

    run = True
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    attack = True

        screen.fill((0, 0, 0))
        if attack:
            if cadr_tick == script[0][choice][script_navigator][1]:
                cadr = script[0][choice][script_navigator][0]
                cadr_tick = 0
                script_navigator += 1
                if script_navigator == len(script[0][choice]):
                    attack = False
                    script_navigator = 0
            for i in range(len(imgs[cadr])):
                screen.blit(imgs[cadr][i], (900 - index[cadr][i][2] * 5 - index[cadr][i][4] * 5, index[cadr][i][5] * 5))
            cadr_tick += 1
        else:
            screen.blit(imgs[0][0], (900 - index[0][0][2] * 5 - index[0][0][4] * 5, index[0][0][5] * 5))

        pygame.display.update()


# test()
