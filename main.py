import pygame
from person import Person
from Player import Player
from settings import *
from dextr import *


def mapping(pos):
    return (pos[0] // TILE, pos[1] // TILE)


class Main:
    def __init__(self):
        self.tick = 0
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('RPG')
        self.clock = pygame.time.Clock()

        self.bg = pygame.image.load('templates/map/map1.png')
        self.bg = pygame.transform.scale(self.bg, (1200, 800))

        self.mouse_pos = (0, 0)

        self.player = Player()

        self.cant = []
        self.graph = None
        self.person_positions = []

    def render(self):
        # bg
        self.screen.blit(self.bg, (0, 0))
        for x in range(0, WIDTH, TILE):
            for y in range(0, HEIGHT, TILE):
                pygame.draw.rect(self.screen, WHITE, (x, y, TILE, TILE), 1)

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

        # persons
        for person in self.player.persons:
            if self.tick % 240 < 120:
                i_ = (self.tick % 120 // 20)
            else:
                i_ = 0
            self.screen.blit(person.state_images[i_], (person.get_big_pos()[0] - 10, person.get_big_pos()[1] - 10))

        # fps
        f1 = pygame.font.Font(None, 40)
        text = f1.render(str(self.clock.get_fps()), True, BLACK)
        self.screen.blit(text, (1150, 0))

    def main_loop(self):
        run = True
        while run:
            self.tick += 1
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
                                    self.graph, self.cant = generate_graph('levels/lvl1.txt', self.person_positions)
                                else:
                                    self.player.choice_person = None
                    else:
                        if self.mouse_pos not in self.cant and self.mouse_pos not in self.person_positions:
                            self.player.persons[self.player.choice_person].move(self.mouse_pos)
                            self.player.choice_person = None

            self.mouse_pos = mapping(pygame.mouse.get_pos())
            main.render()
            pygame.display.update()


main = Main()

main.main_loop()
pygame.quit()
