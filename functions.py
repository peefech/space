import pygame
from config import *
from alien import Alien


def create_alien_fleet(fleet_group):
    """
    Создание флота инопланетян
    """
    alien_count = 0

    for i in range(ROWS):
        if i == 0:
            alien_path = POINTS_30
            points = ALIEN_30_POINTS
        elif i == 1:
            alien_path = POINTS_30
            points = ALIEN_30_POINTS
        elif i == 2:
            alien_path = POINTS_20
            points = ALIEN_20_POINTS
        elif i == 3:
            alien_path = POINTS_20
            points = ALIEN_20_POINTS
        elif i == 4:
            alien_path = POINTS_10
            points = ALIEN_10_POINTS
        else:
            alien_path = POINTS_10
            points = 10

        for j in range(COLUMNS):
            new_alien = Alien((j * 1.5 * ALIEN_WIDTH + SCREEN_WIDTH // 9), i * (2 * ALIEN_HEIGHT) + ALIEN_TOP_OFFSET,
                              i, j, alien_path, points)
            fleet_group.append(new_alien)
            alien_count += 1

    return alien_count


def write_on_screen(text, color, pos, screen, font):
    """
    Писать на экарн
    """
    screen.blit(font.render(text, True, pygame.Color(color)), pos)


def write_one_symbol(text, pos, delay, screen, font):
    """
    Писать по символьно
    """
    for index in range(len(text)):
        write_on_screen(text[index], "white", pos, screen, font)
        pygame.time.delay(delay)
        pos = [pos[0] + 30, pos[1]]
        pygame.display.flip()


def stage_loop():
    loop = True
    while loop:
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    quit()
                elif event.key == pygame.K_RETURN:
                    loop = False


def picture_score(screen):
    aliens_icon = []

    alien_icon_100 = pygame.image.load(POINTS_100).convert_alpha()
    alien_icon_100.set_colorkey(BLACK, pygame.RLEACCEL)
    aliens_icon.append(alien_icon_100)

    alien_icon_30 = pygame.image.load(POINTS_30[1]).convert_alpha()
    alien_icon_30.set_colorkey(BLACK, pygame.RLEACCEL)
    aliens_icon.append(alien_icon_30)

    alien_icon_20 = pygame.image.load(POINTS_20[1]).convert_alpha()
    alien_icon_20.set_colorkey(BLACK, pygame.RLEACCEL)
    aliens_icon.append(alien_icon_20)

    alien_icon_10 = pygame.image.load(POINTS_10[1]).convert_alpha()
    alien_icon_10.set_colorkey(BLACK, pygame.RLEACCEL)
    aliens_icon.append(alien_icon_10)

    for j in range(4):
        life_corner = aliens_icon[j].get_rect(center=(340, 515 + j*80))
        screen.blit(aliens_icon[j], life_corner)
