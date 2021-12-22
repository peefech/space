import pygame
from config import *


class Alien(pygame.sprite.Sprite):

    pygame.mixer.init()
    alien_explosion_sound = pygame.mixer.Sound(ALIEN_EXPLOSION_SOUND)

    def __init__(self, position_x, position_y, row, column, alien_paths, points):
        super().__init__()

        self.alien_paths = alien_paths
        self.surface = pygame.image.load(alien_paths[0]).convert_alpha()
        self.surface.set_colorkey(BLACK, pygame.RLEACCEL)

        self.corner = self.surface.get_rect(center=(position_x, position_y))
        self.row = row
        self.column = column
        self.alien_movement = ALIEN_MOVEMENT
        self.direction = 1
        self.step_down_amount = 0
        self.anim_iterator = 0
        self.destruct_start_time = None
        self.points = points
        self.fleet_group = []

    def update_destroyed(self):
        """
        Проверка не истекло ли время уничтожения
        """
        if self.destruct_start_time and (pygame.time.get_ticks() - self.destruct_start_time >= DESTRUCTION_TIME):
            self.destroy()
            return True
        return False

    def move(self):
        """
        Передвижение
        """
        if not self.update_destroyed():
            self.animate()
            self.corner.move_ip(self.direction * self.alien_movement, self.step_down_amount)

    def animate(self):
        """
        Анимация путем переключения спрайтов
        """
        if self.anim_iterator == 0:
            self.anim_iterator = 1
        else:
            self.anim_iterator = 0
        self.surface = pygame.image.load(self.alien_paths[self.anim_iterator]).convert_alpha()

    def out_of_screen(self):
        """
        Проверка есть ли за границы нахождение
        """
        if self.corner.bottom >= SCREEN_HEIGHT - 70:
            return True
        return False

    def step_down(self):
        """
        Перемещение на 1 ряд ближе к игроку
        """
        if not self.update_destroyed():
            self.step_down_amount += ALIEN_HEIGHT
            self.corner.move_ip(self.direction * self.alien_movement, self.step_down_amount)
            self.step_down_amount = 0

    def destroy(self):
        """
        Уничтожение себя
        """
        position = self.row * COLUMNS + self.column
        self.fleet_group[position] = None
        self.destruct_start_time = None
        self.kill()

    def init_destruction(self, fleet):
        """
        Инициализация уничтожения алиена
        """
        self.surface = pygame.image.load(ALIEN_EXPLOSION).convert_alpha()
        self.surface.set_colorkey(BLACK, pygame.RLEACCEL)
        self.destruct_start_time = pygame.time.get_ticks()
        self.fleet_group = fleet
        self.alien_explosion_sound.play()
