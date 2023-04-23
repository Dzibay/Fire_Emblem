from collections import deque


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
            if cord[0] != 14 and cords[(cord[0] + 1, cord[1])] is not None:
                cords_.append((cord[0] + 1, cord[1]))
            if cord[1] != 0 and cords[(cord[0], cord[1] - 1)] is not None:
                cords_.append((cord[0], cord[1] - 1))
            if cord[1] != 9 and cords[(cord[0], cord[1] + 1)] is not None:
                cords_.append((cord[0], cord[1] + 1))
            cords[cord] = cords_

    return cords, not_zero


def get_cords(graph, start, goal):
    cords = bfs(graph, start, goal)
    return cords
