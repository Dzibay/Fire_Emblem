import pygame


def read(file, weapon, script=False):
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
            if i[0][len(weapon) + 5:len(weapon) + 10] == 'under':
                print(i)
                result[len(result) - 1].append([int(j) for j in i[1:]])
            else:
                result.append([[int(j) for j in i[1:]]])
        return result


def test():
    pygame.init()
    pers = 'mercenary'
    weapon = 'sword'
    choice = 'attack'
    screen = pygame.display.set_mode((1000, 800))
    clock = pygame.time.Clock()
    index = read(open(f'../templates/persons/other/{pers}/man/battle/{weapon}/Index.txt').readlines(), weapon)
    script = read(open(f'../templates/persons/other/{pers}/man/battle/{weapon}/Script.txt').readlines(), weapon, True)
    imgs = [[pygame.transform.flip(pygame.transform.scale(pygame.image.load(f'../templates/persons/other/{pers}/man/battle/{weapon}/attack.png').
            subsurface((i[0], i[1], i[2], i[3])), (i[2] * 5, i[3] * 5)), True, False) for i in j] for j in index]

    death_opacity = [0, 20, 20, 20, 20, 44, 44, 44, 44, 64,
                          64, 64, 64, 84, 84, 84, 108, 108, 108, 108,
                          128, 128, 128, 128, 148, 148, 148, 148, 172, 172,
                          172, 192, 192, 192, 192, 212, 212, 212, 212, 236,
                          236, 236, 236, 255, 255, 255, 0, 0, 0, 0,
                          0, 0, -1, 0, 0, 0, 0, 0, 0, 255,
                          0, 0, 0, 0, 0, 0, 255, 0, 0, 0,
                          0, 0, 0, 255, 0, 0, 0, 0, 0, 0,
                          255, 0, 0, 0, 0, 0, 0]
    print(len(death_opacity))
    cadr = 0
    cadr_tick = 0
    script_navigator = 0
    attack = False
    dead = False
    death_tick = 0

    run = True
    while run:
        clock.tick(50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    attack = True
                elif event.key == pygame.K_RETURN:
                    dead = True

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
        elif dead:
            i_ = imgs[0][0]
            i_.set_alpha(death_opacity[death_tick])
            screen.blit(i_, (900 - index[0][0][2] * 5 - index[0][0][4] * 5, index[0][0][5] * 5))
            if death_tick == len(death_opacity) - 1:
                dead = False
            else:
                death_tick += 1
        else:
            screen.blit(imgs[0][0], (900 - index[0][0][2] * 5 - index[0][0][4] * 5, index[0][0][5] * 5))

        pygame.display.update()


test()
