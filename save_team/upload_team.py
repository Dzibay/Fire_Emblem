def upload_team(name):
    file = open('save_team/saved_teams.txt', 'r').readlines()
    find = False
    result = []
    for line in file:
        line = line[:-1]
        if len(line) == 0:
            find = False

        if find:
            line = line.split()
            data = []
            for i in line:
                try:
                    data.append(int(i))
                except:
                    data.append(i)
            result.append(data)

        if line == name:
            find = True
    return result


def can_save(name):
    file = open('save_team/saved_teams.txt', 'r').readlines()
    res = True
    for line in file:
        if line[:-1] == name:
            res = False
    return res


def save_team(name, datas):
    file = open('save_team/saved_teams.txt', 'a')
    result = []
    line = ''
    for person in datas:
        data_stats = datas[person][0]
        data_weapon = datas[person][1]
        line += f'{person}'
        for stat in data_stats:
            line += f' {data_stats[stat]}'
        for weapon in data_weapon:
            line += f' {weapon}'
        result.append(line)
        line = ''

    print('complited')
    file.write(f'\n')
    file.write(f'{name}\n')
    for i in result:
        file.write(f'{i}\n')
