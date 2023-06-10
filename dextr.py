from collections import deque
from functools import lru_cache


g = {'0': 'plain', '1': 'wall', '2': 'water', '3': 'forest', '4': 'mountain'}

movement_penalties = {'plain': 1,
                      'wall': 1,
                      'water': 1,
                      'forest': 2,
                      'mountain': 5}

maps = ['0000003000003333',
        '0000100300000333',
        '0000000000000033',
        '0110000000000003',
        '0000010000000000',
        '0301100000000040',
        '0030000000000040',
        '3000011001100004',
        '2022210000100004',
        '0000212020100000',
        '0000010022122200',
        '4000010000100202',
        '4300011011100003',
        '4000000000000300',
        '4000000000011030',
        '0000000000100000',
        '3000000000000110',
        '3300000000000000',
        '3330000003010000',
        '3333000030000000']

pay = {}
for y in range(len(maps)):
    for x in range(len(maps[y])):
        pay[(x, y)] = movement_penalties[g[maps[y][x]]]


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
def generate_graph(file, flying):
    not_zero = []
    lvl = open(file, 'r').readlines()
    lvl = [i.replace('\n', '') for i in lvl]
    matrix = [[int(i) for i in j] for j in lvl]
    cords = {(j, i): [] for i in range(len(matrix)) for j in range(len(matrix[0]))}
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            cant = [1] if flying else [1, 2]
            if matrix[i][j] in cant:
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


def get_cords(graph_, start, goal, length, flying=False):
    graph = graph_.copy()
    result = []

    if flying:
        res = bfs(graph, start, goal)
        min_ = len(res) - 1
    else:
        while True:
            cords = bfs(graph, start, goal)
            try:
                pay_ = 0
                cords = [i for i in cords if i != start]
                for cord in cords:
                    pay_ += pay[cord]
                result.append((cords, pay_))
                graph[cords[1]] = []
            except:
                break
        min_ = 1000
        res = []
        for i in result:
            if i[1] != 0:
                if i[1] < min_:
                    min_ = i[1]
                    res = i[0]
        res += [start]
    return res if min_ <= length else []

