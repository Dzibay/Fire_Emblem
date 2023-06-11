import pygame
from settings import WHITE, BLACK, GREY, BLUE, RED, GREEN, YELLOW


def create_new_map(graph):
    res = ['' for i in range(36)]
    line = 0
    for i in graph:
        if i[1] != line:
            line += 1

        if graph[i] is not None:
            res[line] += str(graph[i])
        else:
            res[line] += '.'

    for i in res:
        print(i)


def mapping(pos, cam):
    return ((pos[0] - 100) // 40 + cam[0], pos[1] // 40 + cam[1])


def in_box(pos, rect):
    if pos[0] > rect[0]:
        if pos[0] < rect[0] + rect[2]:
            if pos[1] > rect[1]:
                if pos[1] < rect[1] + rect[3]:
                    return True
    return False


def draw_map():
    pygame.init()
    clock = pygame.time.Clock()
    cam_pos = [0, 0]
    choice_texture = 0
    textures = [(10, 10 + 100 * i, 80, 80) for i in range(5)]
    colors = [YELLOW, BLACK, BLUE, GREEN, RED]
    draw = False

    # settings
    WIDTH, HEIGHT = 1040, 800
    TILE = 40
    map_size = (36, 36)
    map_img = pygame.image.load('new_map.png')

    map_img = pygame.transform.scale(map_img, (map_size[0] * TILE, map_size[1] * TILE))
    bg = map_img.subsurface(cam_pos[0] * TILE, cam_pos[1] * TILE, WIDTH, HEIGHT)
    screen = pygame.display.set_mode((WIDTH + 100, HEIGHT))
    graph = {(x, y): None for y in range(map_size[1]) for x in range(map_size[0])}

    run = True
    while run:
        clock.tick(30)
        pygame.display.set_caption(str(clock.get_fps()))
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    create_new_map(graph)
                elif event.key == pygame.K_w:
                    if cam_pos[1] > 0:
                        cam_pos[1] -= 1
                elif event.key == pygame.K_s:
                    if cam_pos[1] + HEIGHT // TILE < map_size[1]:
                        cam_pos[1] += 1
                elif event.key == pygame.K_d:
                    if cam_pos[0] + WIDTH // TILE < map_size[0]:
                        cam_pos[0] += 1
                elif event.key == pygame.K_a:
                    if cam_pos[0] > 0:
                        cam_pos[0] -= 1
                bg = map_img.subsurface(cam_pos[0] * TILE, cam_pos[1] * TILE, WIDTH, HEIGHT)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                draw = True
            if event.type == pygame.MOUSEBUTTONUP:
                if mouse_pos[0] < 100:
                    for texture in textures:
                        if in_box(mouse_pos, texture):
                            choice_texture = textures.index(texture)
                draw = False
        if draw and mouse_pos[0] > 100:
            graph[mapping(mouse_pos, cam_pos)] = choice_texture

        screen.blit(bg, (100, 0))

        for i in graph:
            if graph[i] is not None:
                rect = pygame.Surface((TILE, TILE))
                rect.fill(colors[graph[i]])
                rect.set_alpha(100)
                screen.blit(rect, ((i[0] - cam_pos[0]) * TILE + 100, (i[1] - cam_pos[1]) * TILE))

        pygame.draw.rect(screen, GREY, (0, 0, 100, HEIGHT))
        for texture in textures:
            pygame.draw.rect(screen, colors[textures.index(texture)], texture)
        if choice_texture is not None:
            pygame.draw.rect(screen, WHITE, textures[choice_texture], 5)

        pygame.display.update()


draw_map()
