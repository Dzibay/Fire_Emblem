from data.persons import characters
from data.weapon import weapon_img
from settings import *
import pygame


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.person_settings = None
        self.list_of_weapon = []
        self.list_of_weapon_see = 0
        self.edit_team_btn = (175, 180, 445, 80)
        self.ally_growth_btn = (175, 285, 445, 80)
        self.equipment_btn = (175, 392, 445, 80)
        self.start_btn = (450, 550, 300, 50)
        self.settings_exit_btn = (700, 600, 200, 50)
        self.tick = 0
        self.phase = 'edit_team'
        self.person_choice_cords = [(i, j, 100, 100) for j in range(300, 730, 120) for i in range(970, 1770, 120)]
        self.all_names_persons = ['roy', 'lyn', 'marth', 'ike', 'eirika',
                                  'eliwood', 'hector', 'dorcas',
                                  'ephraim',
                                  'sophia', 'lina']
        self.choice_persons_weapon = {name: [characters[name]['weapon']] for name in self.all_names_persons}
        self.person_img = [
            pygame.image.load(f'templates/persons/{i}/person/map_idle.png').subsurface((0, 0, 48, 48))
            for i in self.all_names_persons]
        for i in range(len(self.person_img)):
            self.person_img[i] = pygame.transform.scale(self.person_img[i], (200, 200))
        self.choice_persons = []

        self.bg_sky = pygame.transform.scale(pygame.image.load('templates/menu/sky.png').convert_alpha(),
                                             (WIDTH, HEIGHT))
        self.second_sky = pygame.transform.flip(self.bg_sky, True, False)
        self.bg = [pygame.transform.scale(pygame.image.load(f'templates/menu/{i}.png').convert_alpha(), (WIDTH, HEIGHT))
                   for i in range(25)]
        self.x_1 = 0
        self.x_2 = -1920

    def render(self, flag):
        self.tick += 1
        self.x_1 += 1 if self.tick % 2 == 0 else 0
        self.x_2 += 1 if self.tick % 2 == 0 else 0
        if self.x_1 == 1920:
            self.x_1 = -1920
        if self.x_2 == 1920:
            self.x_2 = -1920
        self.screen.blit(self.bg_sky, (self.x_1, 0))
        self.screen.blit(self.second_sky, (self.x_2, 0))
        for img in self.bg[:18]:
            self.screen.blit(img, (0, 0))
        f3 = pygame.font.Font(None, 70)
        f1 = pygame.font.Font(None, 30)
        if flag:
            # person settings
            if self.person_settings is not None:
                text_name = f3.render(self.all_names_persons[self.person_settings], True, WHITE)
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
                    name_weapon = f1.render(weapon_, True, BLACK if c_ == WHITE else WHITE)
                    self.screen.blit(weapon_img[weapon_], (600, 195 + i * 75))
                    self.screen.blit(name_weapon, (700, 220 + i * 75))
            else:
                if self.phase == 'edit_team':
                    for i in range(len(self.person_choice_cords)):
                        c_ = BLUE if self.person_choice_cords[i] in self.choice_persons else WHITE
                        pygame.draw.rect(self.screen, c_, self.person_choice_cords[i])
                        try:
                            self.screen.blit(self.person_img[i], (self.person_choice_cords[i][0] - 50,
                                                                  self.person_choice_cords[i][1] - 50))
                        except:
                            pass
                # pygame.draw.rect(self.screen, GREEN, self.start_btn)

                for i in range(len(self.choice_persons)):
                    self.screen.blit(self.person_img[self.person_choice_cords.index(self.choice_persons[i])],
                                     (1100 + i * 90, 52))
                for img in self.bg[18:]:
                    self.screen.blit(img, (0, 0))
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
            text = f1.render('Waiting the second player...', True, WHITE)
            self.screen.blit(text, (WIDTH // 2 - 140, HEIGHT // 2 + 70))
