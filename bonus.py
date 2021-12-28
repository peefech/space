import pygame
from config import *
import random


class Bonus(pygame.sprite.Sprite):

    def __init__(self, position):
        super().__init__()

        self.surface = pygame.image.load(BONUS).convert_alpha()
        self.surface.set_colorkey(BLACK, pygame.RLEACCEL)

        self.time_active = pygame.time.get_ticks()
        self.active = False
        self.anim_iterator = 0
        self.random_num = None
        self.speed_bust = False
        self.corner = self.surface.get_rect(center=position)
        self.reload_bust = 1

    def activate(self, spaceship):
        self.time_active = pygame.time.get_ticks()
        self.random_num = random.randint(0, 2)
        self.active = True

        # щит
        if self.random_num == 0:
            spaceship.sheet = True
            spaceship.surface = pygame.image.load(SHEET_SPACESHIP[0]).convert_alpha()
            spaceship.surface.set_colorkey(WHITE)

        # ускорение пуль
        if self.random_num == 1:
            self.speed_bust = True

        # быстрее перезарядка
        if self.random_num == 2:
            self.reload_bust = 2

    def update(self, spaceship):
        if pygame.time.get_ticks() - self.time_active >= BONUS_DESTRUCTION_TIME:
            self.destroy(spaceship)

    def update_sheet(self, spaceship):
        if self.anim_iterator == 0:
            self.anim_iterator = 1
        else:
            self.anim_iterator = 0
        spaceship.surface = pygame.image.load(SHEET_SPACESHIP[self.anim_iterator]).convert_alpha()
        spaceship.surface.set_colorkey(WHITE)

    def destroy(self, spaceship):
        if self.random_num == 0:
            spaceship.sheet = False
            spaceship.surface = pygame.image.load(SPACESHIP_PATH).convert_alpha()
            spaceship.surface.set_colorkey(WHITE)

        if self.random_num == 1:
            self.speed_bust = False

        if self.random_num == 2:
            self.reload_bust = 1

        self.kill()
