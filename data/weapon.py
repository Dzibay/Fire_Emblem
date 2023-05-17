import pygame

weapon = {'iron_sword': {'mt': 5, 'wt': 5, 'hit': 90, 'crt': 0, 'range': [1], 'class': 'sword'},
          'iron_axe': {'mt': 8, 'wt': 10, 'hit': 75, 'crt': 0, 'range': [1], 'class': 'axe'},
          'iron_lance': {'mt': 7, 'wt': 8, 'hit': 80, 'crt': 0, 'range': [1], 'class': 'lance'},
          'bow': {'mt': 6, 'wt': 5, 'hit': 80, 'crt': 0, 'range': [2], 'class': 'bow'},
          'flux': {'mt': 5, 'wt': 4, 'hit': 95, 'crt': 0, 'range': [1, 2], 'class': 'magic'}}

weapon_img = {
    'iron_sword': pygame.transform.scale(pygame.image.load('templates/weapon/weapon.png').subsurface((16, 0, 16, 16)),
                                         (72, 72)),
    'iron_axe': pygame.transform.scale(pygame.image.load('templates/weapon/weapon.png').subsurface((119, 51, 16, 16)),
                                       (72, 72)),
    'iron_lance': pygame.transform.scale(pygame.image.load('templates/weapon/weapon.png').subsurface((34, 34, 16, 16)),
                                         (72, 72)),
    'bow': pygame.transform.scale(pygame.image.load('templates/weapon/weapon.png').subsurface((51, 85, 16, 16)),
                                  (72, 72)),
    'flux': pygame.transform.scale(pygame.image.load('templates/weapon/weapon.png').subsurface((51, 119, 16, 16)),
                                   (72, 72))}

weapon_arrow = {'up': [pygame.transform.scale(pygame.image.load('templates/fight/up_arrow.png').
                                              subsurface(x * 7, 0, 7, 10), (32, 45)) for x in range(3)],
                'down': [pygame.transform.scale(pygame.image.load('templates/fight/down_arrow.png').
                                                subsurface(x * 7, 0, 7, 10), (32, 45)) for x in range(3)]}
