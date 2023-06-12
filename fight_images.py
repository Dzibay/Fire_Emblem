import pygame
from data.persons import characters
from data.magic import magic
from person import lords

magic_names = ['sophia', 'lina']


class Fight_images:
    def __init__(self):
        self.images = {}
        self.magic_effects = {}
        self.uploaded_images = False

    def read(self, file, weapon_='', script=False):
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
                    elif i[:12] == 'wait_for_hit':
                        dmg_end = True
                    elif len(i) == 1 and len(res) > 1:
                        break
                result[attack] = [[int(i[2].split('_')[1]), int(i[1])] for i in res]
                result[attack] = [[i[0] - result[attack][0][0], i[1]] for i in result[attack]]
                dmg_times[attack] = dmg_time

            return result, dmg_times
        else:
            res = [[i[:-1].split(';')[0]] + i[:-1].split(';')[1].split(',') +
                   i[:-1].split(';')[2].split(',') + i[:-1].split(';')[3].split(',')
                   for i in file]
            result = []
            for i in res:
                if i[0][len(weapon_) + 5:len(weapon_) + 10] == 'under':
                    result[len(result) - 1].append([int(j) for j in i[1:]])
                else:
                    result.append([[int(j) for j in i[1:]]])
            return result

    def upload_images(self, names):
        for person in names:
            h_ = person.split('/')
            name = h_[0]
            class_ = h_[1]
            if name not in self.images:
                if name in magic_names and not self.uploaded_images:
                    self.uploaded_images = True
                    # magic
                    for magic_ in magic:
                        self.magic_effects[magic_] = {'person': [], 'enemy': []}
                        # enemy magic
                        self.magic_effects[magic_]['enemy'] = [pygame.transform.scale(
                            pygame.image.load(f'templates/magic/{magic_}.png').convert_alpha().
                            subsurface(x * magic[f'{magic_}']['width'], y * magic[f'{magic_}']['height'],
                                       magic[f'{magic_}']['width'], magic[f'{magic_}']['height']),
                            magic[f'{magic_}']['size'])
                                                                  for y in range(magic[f'{magic_}']['h'])
                                                                  for x in range(magic[f'{magic_}']['w'])][
                                                              :magic[f'{magic_}']['frames']]

                        # person magic
                        self.magic_effects[magic_]['person'] = [pygame.transform.flip(i, True, False)
                                                                for i in self.magic_effects[magic_]['enemy']]

                # persons
                if name in lords:
                    w_ = characters[name]['can_use' if class_ == characters[name]['class'] else 't2_can_use']
                    # if 'lance' in w_:
                    #     w_.append('distance_lance')
                    # if 'axe' in w_:
                    #     w_.append('distance_axe')
                    t_ = 1 if class_ == characters[name]['class'] else 2
                    self.images[person] = {i: [] for i in w_}
                    for weapon_ in w_:
                        self.images[person][weapon_] = {'person': [], 'enemy': []}
                        index = self.read(open(f'templates/persons/lords/{name}/battle/T{t_}/{weapon_}/Index.txt').readlines(), weapon_)
                        enemy_attack_img = []
                        image = pygame.image.load(f'templates/persons/lords/{name}/battle/T{t_}/{weapon_}/attack.png').convert_alpha()
                        for j in index:
                            ar_ = []
                            for i in j:
                                img = pygame.transform.scale(image.subsurface((i[0], i[1], i[2], i[3])), (i[2] * 5, i[3] * 5))
                                ar_.append(img)
                            enemy_attack_img.append(ar_)
                        # person
                        person_attack_img = [[pygame.transform.flip(img, True, False) for img in array] for array in enemy_attack_img]

                        self.images[person][weapon_]['person'] = person_attack_img
                        self.images[person][weapon_]['enemy'] = enemy_attack_img
                else:
                    try:
                        w_ = characters[name]['can_use' if class_ == characters[name]['class'] else 't2_can_use']
                        # if 'lance' in w_:
                        #     w_.append('distance_lance')
                        # if 'axe' in w_:
                        #     w_.append('distance_axe')
                        self.images[person] = {i: [] for i in w_}
                        for weapon_ in w_:
                            self.images[person][weapon_] = {'person': [], 'enemy': []}
                            index = self.read(open(f'templates/persons/other/{class_}/{name}/battle/{weapon_}/Index.txt').readlines(), weapon_)
                            enemy_attack_img = []
                            image = pygame.image.load(f'templates/persons/other/{class_}/{name}/battle/{weapon_}/attack.png').convert_alpha()
                            for j in index:
                                ar_ = []
                                for i in j:
                                    img = pygame.transform.scale(image.subsurface((i[0], i[1], i[2], i[3])), (i[2] * 5, i[3] * 5))
                                    ar_.append(img)
                                enemy_attack_img.append(ar_)
                            # person
                            person_attack_img = [[pygame.transform.flip(img, True, False) for img in array] for array in enemy_attack_img]

                            self.images[person][weapon_]['person'] = person_attack_img
                            self.images[person][weapon_]['enemy'] = enemy_attack_img
                    except:
                        w_ = characters[name]['can_use' if class_ == characters[name]['class'] else 't2_can_use']
                        g_ = characters[name]['gender']
                        self.images[person] = {i: [] for i in w_}
                        for weapon_ in w_:
                            self.images[person][weapon_] = {'person': [], 'enemy': []}
                            index = self.read(
                                open(f'templates/persons/other/{class_}/{g_}/battle/{weapon_}/Index.txt').readlines(),
                                weapon_)
                            enemy_attack_img = []
                            image = pygame.image.load(
                                f'templates/persons/other/{class_}/{g_}/battle/{weapon_}/attack.png').convert_alpha()
                            for j in index:
                                ar_ = []
                                for i in j:
                                    img = pygame.transform.scale(image.subsurface((i[0], i[1], i[2], i[3])),
                                                                 (i[2] * 5, i[3] * 5))
                                    ar_.append(img)
                                enemy_attack_img.append(ar_)
                            # person
                            person_attack_img = [[pygame.transform.flip(img, True, False) for img in array] for array in
                                                 enemy_attack_img]

                            self.images[person][weapon_]['person'] = person_attack_img
                            self.images[person][weapon_]['enemy'] = enemy_attack_img