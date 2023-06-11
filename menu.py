import pygame
from numba import jit
from settings import *
from data.persons import characters
from data.weapon import weapon_img, weapon
from random import randint
from data.classes import classes_bonus


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.person_settings = None
        self.ally_growth_person = None
        self.list_of_weapon = []
        self.list_of_weapon_see = 0
        self.edit_team_btn = (175, 180, 445, 80)
        self.ally_growth_btn = (175, 285, 445, 80)
        self.equipment_btn = (175, 392, 445, 80)
        self.start_btn = (175, 792, 445, 80)
        self.settings_exit_btn = (700, 600, 200, 50)
        self.lvl_up_btn = (1240, 622, 30, 30)
        self.up_class_btns = [(1250, 700, 300, 50),
                              (1250, 760, 300, 50)]
        self.run = True
        self.placing_persons_window = False
        self.tick = 0
        self.sms = ''
        self.phase = 'edit_team'
        self.person_choice_cords = [(i, j, 100, 100) for j in range(300, 730, 120) for i in range(970, 1770, 120)]
        self.all_names_persons = ['roy', 'lyn', 'marth', 'ike', 'eirika', 'eliwood', 'hector',
                                  'ephraim', 'barthe', 'amelia', 'kent', 'wil', 'florina', 'marisa',
                                  'raven', 'rath', 'heath', 'sophia', 'lina']
        self.up_classes = {name: False for name in self.all_names_persons}

        self.choice_persons_weapon = {name: [characters[name]['weapon']] for name in self.all_names_persons}
        self.result_person_stats = {name: {'lvl': characters[name]['lvl'],
                                           'hp': characters[name]['hp'],
                                           'str': characters[name]['str'],
                                           'mag': characters[name]['mag'],
                                           'speed': characters[name]['speed'],
                                           'def': characters[name]['def'],
                                           'res': characters[name]['res'],
                                           'lck': characters[name]['lck'],
                                           'skl': characters[name]['skl'],
                                           'con': characters[name]['con'],
                                           'move': characters[name]['move'],
                                           'class': characters[name]['class']} for name in self.all_names_persons}
        self.ally_growth_stats_cords = {'lvl': (1180, 622),
                                        'hp': (1160, 665),
                                        'str': (1160, 702),
                                        'mag': (1160, 702),
                                        'speed': (1160, 739),
                                        'def': (1160, 778),
                                        'res': (1160, 817),
                                        'lck': (1160, 854),
                                        'skl': (1160, 891),
                                        'con': (1160, 928),
                                        'class': (1300, 700)}

        f_ = [pygame.image.load(f'templates/persons/mugshots/{i}.png').convert_alpha() for i in self.all_names_persons]
        self.person_faces = [pygame.transform.scale(i, (100, 100)) for i in f_]
        self.mini_person_faces = [pygame.transform.scale(i, (70, 70)) for i in f_]
        self.choice_persons = []

        # bg
        self.bg_sky = pygame.transform.scale(pygame.image.load('templates/menu/base/sky.png').convert_alpha(),
                                             (WIDTH, HEIGHT))
        self.second_sky = pygame.transform.flip(self.bg_sky, True, False)
        self.bg = {
            'base': [pygame.transform.scale(pygame.image.load(f'templates/menu/base/{i}.png').
                                            convert_alpha(), (WIDTH, HEIGHT)) for i in ['first', 'second']],
            'edit_team': pygame.transform.scale(pygame.image.load(f'templates/menu/edit_team/0.png').convert_alpha(), (WIDTH, HEIGHT)),
            'ally_growth': pygame.transform.scale(pygame.image.load(f'templates/menu/ally_growth/all.png').convert_alpha(), (WIDTH, HEIGHT))}
        self.x_1 = 0
        self.x_2 = -1920

        self.save_team_btn = (900, 130, 100, 50)
        self.upload_team_btn = (730, 130, 150, 50)
        self.save_upload_text = ''
        self.save_upload_text_flag = False
        self.save_upload_text_btn = (730, 80, 270, 40)

        # fonts
        self.f1 = pygame.font.Font(None, 30)
        self.f2 = pygame.font.Font(None, 50)
        self.f3 = pygame.font.Font(None, 70)
        self.f1_f2 = pygame.font.Font(None, 40)

    def change_class(self, id_):
        self.choice_persons_weapon[self.ally_growth_person] = \
            [i for i in self.choice_persons_weapon[self.ally_growth_person]
             if weapon[i]['class'] in characters[self.ally_growth_person]['can_use'
            if self.result_person_stats[self.ally_growth_person]['lvl'] < 10 else 't2_can_use']]

        class_ = characters[self.ally_growth_person]['up_to'][id_]
        self.result_person_stats[self.ally_growth_person]['class'] = class_
        for stat in classes_bonus[class_]:
            self.result_person_stats[self.ally_growth_person][stat] += classes_bonus[class_][stat]

        self.up_classes[self.ally_growth_person] = False

    def change_lvl(self):
        self.result_person_stats[self.ally_growth_person]['lvl'] += 1
        for stat in characters[self.ally_growth_person]['rates']:
            self.result_person_stats[self.ally_growth_person][stat] += 1 if randint(0, 100) < \
                                                                            characters[self.ally_growth_person][
                                                                                'rates'][stat] else 0
        if self.result_person_stats[self.ally_growth_person]['lvl'] == 10:
            if len(characters[self.ally_growth_person]['up_to']) < 2:
                self.change_class(0)
            else:
                self.up_classes[self.ally_growth_person] = True

    def render(self, person_settings):
        self.tick += 1
        self.x_1 += 1 if self.tick % 3 == 0 else 0
        self.x_2 += 1 if self.tick % 3 == 0 else 0
        if self.x_1 == 1920:
            self.x_1 = -1920
        if self.x_2 == 1920:
            self.x_2 = -1920
        self.screen.blit(self.bg_sky, (self.x_1, 0))
        self.screen.blit(self.second_sky, (self.x_2, 0))
        self.screen.blit(self.bg['base'][0], (0, 0))

        if person_settings:
            # person settings
            if self.person_settings is not None:
                self.screen.fill(GREY)
                text_name = self.f3.render(self.all_names_persons[self.person_settings], True, WHITE)
                self.screen.blit(text_name, (500, 100))
                pygame.draw.rect(self.screen, RED, self.settings_exit_btn)
                # person list weapon
                l_ = self.choice_persons_weapon[self.all_names_persons[self.person_settings]]
                for i in range(len(l_)):
                    pygame.draw.rect(self.screen, WHITE, (300, 200 + i * 75, 200, 72))
                    self.screen.blit(weapon_img[l_[i]], (300, 195 + i * 75))
                # list all weapon
                for weapon_ in self.list_of_weapon[self.list_of_weapon_see:self.list_of_weapon_see + 5]:
                    i = self.list_of_weapon[
                        self.list_of_weapon_see:self.list_of_weapon_see + 5].index(weapon_)
                    c_ = BLACK if weapon_ in l_ else WHITE
                    pygame.draw.rect(self.screen, c_, (600, 200 + i * 75, 300, 72))
                    name_weapon = self.f1.render(weapon_, True, BLACK if c_ == WHITE else WHITE)
                    self.screen.blit(weapon_img[weapon_], (600, 195 + i * 75))
                    self.screen.blit(name_weapon, (700, 220 + i * 75))
            else:
                if self.phase == 'edit_team':
                    self.screen.blit(self.bg['edit_team'], (0, 0))
                    for i in range(len(self.person_choice_cords)):
                        c_ = BLUE if self.person_choice_cords[i] in self.choice_persons else WHITE
                        pygame.draw.rect(self.screen, c_, self.person_choice_cords[i])
                        try:
                            self.screen.blit(self.person_faces[i], (self.person_choice_cords[i][0],
                                                                    self.person_choice_cords[i][1]))
                        except:
                            pass

                    # save/upload team
                    pygame.draw.rect(self.screen, BLUE, self.upload_team_btn)
                    pygame.draw.rect(self.screen, GREEN, self.save_team_btn)
                    text_upload = self.f2.render('Upload', True, WHITE)
                    text_save = self.f2.render('Save', True, WHITE)
                    self.screen.blit(text_upload, (self.upload_team_btn[0] + 15, self.upload_team_btn[1] + 10))
                    self.screen.blit(text_save, (self.save_team_btn[0] + 10, self.save_team_btn[1] + 10))

                    pygame.draw.rect(self.screen, WHITE, self.save_upload_text_btn)
                    text = self.f2.render(self.save_upload_text, True, BLACK)
                    self.screen.blit(text, (self.save_upload_text_btn[0] + 10, self.save_upload_text_btn[1] + 5))

                    if self.save_upload_text_flag:
                        if self.tick % 40 < 15:
                            pygame.draw.rect(self.screen, BLACK,
                                             (self.save_upload_text_btn[0] + 10 + len(self.save_upload_text) * 21,
                                              self.save_upload_text_btn[1] + 2, 2, 36))
                elif self.phase == 'ally_growth':
                    self.screen.blit(self.bg['ally_growth'], (0, 0))
                    for stat in self.result_person_stats[self.ally_growth_person]:
                        if stat != 'move':
                            if stat != 'class':
                                if stat == 'str' or stat == 'mag':
                                    stat = 'str' if self.result_person_stats[self.ally_growth_person]['str'] > \
                                                    self.result_person_stats[self.ally_growth_person]['mag'] else 'mag'
                                text = self.f2.render(str(self.result_person_stats[self.ally_growth_person][stat]), True,
                                                      WHITE)
                                c_ = self.ally_growth_stats_cords[stat]
                                if stat != 'class':
                                    c_ = c_ if self.result_person_stats[self.ally_growth_person][stat] > 9 \
                                        else (c_[0] + 20, c_[1])
                                self.screen.blit(text, c_)
                            else:
                                if self.up_classes[self.ally_growth_person]:
                                    pass
                                else:
                                    text = self.f2.render(str(self.result_person_stats[self.ally_growth_person]['class']), True, WHITE)
                                    self.screen.blit(text, self.ally_growth_stats_cords['class'])
                    if not self.up_classes[self.ally_growth_person]:
                        pygame.draw.rect(self.screen, GREEN, self.lvl_up_btn)
                    else:
                        for i in range(len(self.up_class_btns)):
                            pygame.draw.rect(self.screen, GREEN, self.up_class_btns[i])
                            text = self.f2.render(characters[self.ally_growth_person]['up_to'][i], True, WHITE)
                            self.screen.blit(text, (self.up_class_btns[i][0] + 20, self.up_class_btns[i][1] + 10))

            for i in range(len(self.choice_persons)):
                self.screen.blit(self.mini_person_faces[self.person_choice_cords.index(self.choice_persons[i])],
                                 (1165 + i * 90, 120))

            self.screen.blit(self.bg['base'][1], (0, 0))

        else:
            i_ = self.tick % 160 // 20
            if i_ == 1:
                cords = [(WIDTH // 2 - 50, HEIGHT // 2 - 50, 50, 50)]
            elif i_ == 2:
                cords = [(WIDTH // 2 - 50, HEIGHT // 2 - 50, 50, 50),
                         (WIDTH // 2, HEIGHT // 2, 50, 50)]
            elif i_ == 3:
                cords = [(WIDTH // 2 - 50, HEIGHT // 2 - 50, 50, 50),
                         (WIDTH // 2, HEIGHT // 2 - 50, 50, 50),
                         (WIDTH // 2, HEIGHT // 2, 50, 50)]
            elif i_ == 4:
                cords = [(WIDTH // 2 - 50, HEIGHT // 2 - 50, 50, 50),
                         (WIDTH // 2, HEIGHT // 2 - 50, 50, 50),
                         (WIDTH // 2, HEIGHT // 2, 50, 50),
                         (WIDTH // 2 - 50, HEIGHT // 2, 50, 50)]
            elif i_ == 5:
                cords = [(WIDTH // 2, HEIGHT // 2 - 50, 50, 50),
                         (WIDTH // 2, HEIGHT // 2, 50, 50),
                         (WIDTH // 2 - 50, HEIGHT // 2, 50, 50)]
            elif i_ == 6:
                cords = [(WIDTH // 2, HEIGHT // 2 - 50, 50, 50),
                         (WIDTH // 2 - 50, HEIGHT // 2, 50, 50)]
            elif i_ == 7:
                cords = [(WIDTH // 2 - 50, HEIGHT // 2, 50, 50)]
            else:
                cords = []
            for i in cords:
                pygame.draw.rect(self.screen, WHITE, i)
            text = self.f1.render('Waiting the second player...', True, WHITE)
            self.screen.blit(text, (WIDTH // 2 - 140, HEIGHT // 2 + 70))

