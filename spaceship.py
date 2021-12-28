import pygame
from config import *
import time


class SpaceShip:
    def __init__(self, spaceship_path=SPACESHIP_PATH):

        self.surface = pygame.image.load(spaceship_path).convert_alpha()
        self.surface.set_colorkey(WHITE)

        self.lives = LIVES

        self.corner = self.surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 120))
        self.speed = SPACESHIP_MOVEMENT_SPEED
        self.direction = 0

        self.last_shot = 0
        self.destruct_start_time = None
        self.explosion = 1
        self.explosion_time = None

        self.sheet = False

    def control(self, pressed_keys, reload_bust):
        """
        Управление кораблем и стрельбой
        """
        self.direction = 0
        shoot = False
        if pressed_keys[pygame.K_LEFT] or pressed_keys[pygame.K_a]:
            self.corner.move_ip(-self.speed, 0)
            self.direction = - 1
        if pressed_keys[pygame.K_RIGHT] or pressed_keys[pygame.K_d]:
            self.corner.move_ip(self.speed, 0)
            self.direction = 1

        if pressed_keys[pygame.K_SPACE] or pressed_keys[pygame.K_UP]:
            if time.time() - self.last_shot > SHOT_DELAY / reload_bust:
                self.last_shot = time.time()
                shoot = True

        if self.corner.left < 0:
            self.corner.left = 0
        if self.corner.right > SCREEN_WIDTH:
            self.corner.right = SCREEN_WIDTH

        return shoot

    def remove_life(self):
        """
        Убрать жизнь
        """
        self.init_destruction()
        self.lives -= 1

    def init_destruction(self):
        """
        Инициализация уничтожения, подмена спрайта
        """
        self.explosion_time = pygame.time.get_ticks()
        self.destruct_start_time = pygame.time.get_ticks()
        self.surface = pygame.image.load(SPACESHIP_EXPLOSION_1).convert_alpha()

    def update_destroyed(self):
        """
        Проверка истечения таймера, чем дальше, тем больше времени прошло:
        Либо смена спрайта уничтожения
        Либо убрать спрайт
        Либо дать новую жизнь
        """
        if self.destruct_start_time and (
                pygame.time.get_ticks() - self.destruct_start_time >= SPACESHIP_DESTRUCTION_TIME):
            self.new_life()
            return True
        elif self.destruct_start_time and (
                pygame.time.get_ticks() - self.destruct_start_time >= SPACESHIP_DESTRUCTION_TIME - SPACESHIP_DOWNTIME):
            self.surface = None
        elif pygame.time.get_ticks() - self.explosion_time >= SPACESHIP_EXPLOSION_TIME:
            if self.explosion == 1:
                self.surface = pygame.image.load(SPACESHIP_EXPLOSION_2).convert_alpha()
                self.explosion = 2
                self.explosion_time = pygame.time.get_ticks()
            else:
                self.surface = pygame.image.load(SPACESHIP_EXPLOSION_1).convert_alpha()
                self.explosion = 1
                self.explosion_time = pygame.time.get_ticks()
        return False

    def new_life(self):
        """
        Отображение спрайта корабля и сброс таймеров
        """
        self.surface = pygame.image.load(SPACESHIP_PATH).convert_alpha()
        self.explosion_time = None
        self.destruct_start_time = None
