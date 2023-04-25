from settings import *
import pygame

img_cords = [(7, 89, 43, 43), (52, 89, 43, 43), (97, 89, 43, 43), (140, 89, 43, 43), (181, 89, 43, 43),
             (226, 89, 78, 43), (309, 89, 65, 43), (377, 89, 62, 43), (443, 89, 63, 43), (14, 152, 57, 43),
             (74, 152, 52, 43), (127, 152, 44, 43), (174, 152, 36, 43), (219, 152, 38, 43), (274, 152, 42, 43),
             (328, 152, 37, 43), (369, 152, 35, 50), (407, 152, 33, 50), (439, 152, 49, 43), (30, 200, 32, 50),
             (66, 200, 44, 50), (112, 200, 46, 50), (160, 200, 47, 50), (211, 200, 48, 50), (262, 200, 48, 50),
             (312, 200, 47, 50), (358, 200, 38, 50), (402, 200, 39, 50), (444, 200, 42, 50)]


class Fight:
    def __init__(self):
        self.fight_bg = pygame.image.load('templates/fight_bg/bg.png').subsurface((2, 2, 240, 160))
        self.fight_bg = pygame.transform.scale(self.fight_bg, (WIDTH, HEIGHT))

        self.person_img = pygame.image.load('templates/persons_fight/eliwood(lord)/img_B.png')
        self.person_stay_img = self.person_img.subsurface(9, 25, 43, 43)
        self.person_melee_attack_img = [self.person_img.subsurface(i) for i in img_cords]

        self.person_stay_img = pygame.transform.scale(self.person_stay_img, (200, 200))
        self.person_stay_img = pygame.transform.flip(self.person_stay_img, True, False)
        for i in range(len(self.person_melee_attack_img)):
            self.person_melee_attack_img[i] = pygame.transform.scale(self.person_melee_attack_img[i], (200, 200))

            self.person_melee_attack_img[i] = pygame.transform.flip(self.person_melee_attack_img[i], True, False)


        self.enemy_img = pygame.image.load('templates/persons_fight/eliwood(lord)/img_R.png')
        self.enemy_stay_img = self.enemy_img.subsurface(9, 25, 43, 43)
        self.enemy_melee_attack_img = [self.enemy_img.subsurface(i) for i in img_cords]

        self.enemy_stay_img = pygame.transform.scale(self.enemy_stay_img, (200, 200))
        for i in range(len(self.enemy_melee_attack_img)):
            self.enemy_melee_attack_img[i] = pygame.transform.scale(self.enemy_melee_attack_img[i], (200, 200))

        self.tick = 0
        self.person_x, self.person_y = 200, 400
        self.enemy_x, self.enemy_y = 700, 400
        self.speed = 2
        self.person_img_id = 0
        self.enemy_img_id = 0

    def mellee_person_attack(self):
        self.tick += 1
        img = self.person_melee_attack_img[self.tick % (290 // self.speed) // (10 // self.speed)]

        if self.tick < 50 / self.speed:
            pass
        elif self.tick < 100 / self.speed:
            self.person_x += 8 * self.speed
        elif self.tick < 200 / self.speed:
            pass
        elif self.tick < 290 / self.speed:
            self.person_x -= 4.5 * self.speed
        if self.tick == 290 / self.speed:
            self.tick = 0

        if (self.tick > 100 / self.speed) and (self.tick < 140 / self.speed):
            self.person_x -= 1 * self.speed
        elif (self.tick > 200 / self.speed) and (self.tick < 240 / self.speed):
            self.person_y -= 2 * self.speed
        elif self.tick >= 240 / self.speed:
            self.person_y += 1 * self.speed

        return img, (self.person_x, self.person_y)

    def mellee_enemy_attack(self):
        self.tick += 1
        img = self.enemy_melee_attack_img[self.tick % (290 // self.speed) // (10 // self.speed)]

        if self.tick < 50 / self.speed:
            pass
        elif self.tick < 100 / self.speed:
            self.enemy_x -= 8 * self.speed
        elif self.tick < 200 / self.speed:
            pass
        elif self.tick < 290 / self.speed:
            self.enemy_x += 4.5 * self.speed
        if self.tick == 290 / self.speed:
            self.tick = 0

        if (self.tick > 100 / self.speed) and (self.tick < 140 / self.speed):
            self.enemy_x += 1 * self.speed
        elif (self.tick > 200 / self.speed) and (self.tick < 240 / self.speed):
            self.enemy_y -= 2 * self.speed
        elif self.tick >= 240 / self.speed:
            self.enemy_y += 1 * self.speed

        return img, (self.enemy_x, self.enemy_y)

