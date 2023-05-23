from data.persons import characters
import pygame


class Menu:
    def __init__(self):
        self.person_settings = None
        self.list_of_weapon = []
        self.list_of_weapon_see = 0
        self.start_btn = (450, 550, 300, 50)
        self.settings_exit_btn = (700, 600, 200, 50)
        self.tick = 0
        self.person_choice_cords = [(i, j, 100, 100) for j in range(50, 530, 120) for i in range(250, 950, 120)]
        self.all_names_persons = ['roy', 'lyn', 'marth', 'ike', 'hero',
                                  'hector', 'warrior',
                                  'eirika', 'ephraim', 'eliwood',
                                  'sorcerer', 'sagem']
        self.choice_persons_weapon = {name: [characters[name]['weapon']] for name in self.all_names_persons}
        self.person_img = [
            pygame.image.load(f'templates/persons/{i}/person/map_idle.png').subsurface((0, 0, 48, 48))
            for i in self.all_names_persons]
        for i in range(len(self.person_img)):
            self.person_img[i] = pygame.transform.scale(self.person_img[i], (200, 200))
        self.choice_persons = []
