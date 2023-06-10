from collections import deque
from functools import lru_cache
g = {'0': 'plain', '1': 'wall', '2': 'water', '3': 'forest', '4': 'mountain'}

def_buff = {'plain': 0,
            'wall': 0,
            'water': 0,
            'forest': 1,
            'mountain': 2}

avoid_buff = {'plain': 0,
              'wall': 0,
              'water': 0,
              'forest': 20,
              'mountain': 30}

movement_penalties = {'plain': 1,
                      'wall': 1,
                      'water': 1,
                      'forest': 2,
                      'mountain': 3}

lvl = ['0' * 36 for i in range(36)]

pay = {}
for y in range(len(lvl)):
    for x in range(len(lvl[y])):
        pay[(x, y)] = movement_penalties[g[lvl[y][x]]]

lvl_generate = {}
for y in range(len(lvl)):
    for x in range(len(lvl[y])):
        lvl_generate[(x, y)] = g[lvl[y][x]]


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
def generate_graph(flying):
    not_zero = []
    matrix = [[int(i) for i in j] for j in lvl]
    for y_ in range(len(matrix)):
        for x_ in range(len(matrix[y_])):
            if matrix[y_][x_] in [3, 4]:
                matrix[y_][x_] = 0
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
            if cord[0] != 35 and cords[(cord[0] + 1, cord[1])] is not None:
                cords_.append((cord[0] + 1, cord[1]))
            if cord[1] != 0 and cords[(cord[0], cord[1] - 1)] is not None:
                cords_.append((cord[0], cord[1] - 1))
            if cord[1] != 35 and cords[(cord[0], cord[1] + 1)] is not None:
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
