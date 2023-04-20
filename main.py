import pygame
from person import Person
from Player import Player
from settings import *
from dextr import *


def mapping(pos):
    return (pos[0] // TILE, pos[1] // TILE)


class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('RPG')
        self.clock = pygame.time.Clock()

        self.bg = pygame.image.load('templates/map/map1.png')
        self.bg = pygame.transform.scale(self.bg, (1200, 800))

        self.mouse_pos = (0, 0)

        self.player = Player()

        self.graph = None
        self.person_positions = []

    def render(self):
        # bg
        self.screen.blit(self.bg, (0, 0))
        for x in range(0, WIDTH, TILE):
            for y in range(0, HEIGHT, TILE):
                pygame.draw.rect(self.screen, WHITE, (x, y, TILE, TILE), 1)

        # players
        for person in self.player.persons:
            self.screen.blit(person.images['state'], person.get_big_pos())

        # mouse
        pygame.draw.rect(self.screen, BLACK, (self.mouse_pos[0] * TILE, self.mouse_pos[1] * TILE, TILE, TILE), 1)
        if self.player.choice_person is not None:
            p_ = self.player.persons[self.player.choice_person]
            pygame.draw.rect(self.screen, ORANGE, (p_.get_big_pos()[0], p_.get_big_pos()[1], TILE, TILE), 3)

            if self.mouse_pos not in self.person_positions:
                cords = get_cords(self.graph, p_.pos, self.mouse_pos)
                for cord in cords:
                    pygame.draw.circle(self.screen, ORANGE,
                                       (cord[0] * TILE + TILE // 2, cord[1] * TILE + TILE // 2), TILE // 4)

        # fps
        f1 = pygame.font.Font(None, 40)
        text = f1.render(str(self.clock.get_fps()), True, BLACK)
        self.screen.blit(text, (1150, 0))

    def main_loop(self):
        run = True
        while run:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if self.player.choice_person is None:
                        for person in self.player.persons:
                            if self.mouse_pos == person.pos:
                                if self.player.choice_person is None:
                                    self.player.choice_person = self.player.persons.index(person)
                                    self.person_positions = [person.pos for person in self.player.persons
                                                             if person != self.player.persons[self.player.choice_person]]
                                    self.graph = generate_graph('levels/lvl1.txt', self.person_positions)
                                else:
                                    self.player.choice_person = None
                    else:
                        if self.mouse_pos not in self.person_positions:
                            self.player.persons[self.player.choice_person].move(self.mouse_pos)
                            self.player.choice_person = None

            self.mouse_pos = mapping(pygame.mouse.get_pos())
            main.render()
            pygame.display.update()


main = Main()

main.main_loop()
pygame.quit()
