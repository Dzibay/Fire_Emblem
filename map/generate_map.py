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

