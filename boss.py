import pygame
from config import *
import random


class Boss(pygame.sprite.Sprite):
    pygame.mixer.init()
    boss_explosion_sound = pygame.mixer.Sound(BOSS_EXPLOSION_SOUND)
    pygame.mixer.music.load(BOSS_SOUND)

    def __init__(self, position_y=ALIEN_BOSS_Y_POS):
        super().__init__()

        self.surface = pygame.image.load(POINTS_100).convert_alpha()
        self.surface.set_colorkey(BLACK, pygame.RLEACCEL)

        random_num = random.randint(0, 1)
        self.start_x = (- ALIEN_BOSS_WIDTH // 2, SCREEN_WIDTH + ALIEN_BOSS_WIDTH // 2)
        self.corner = self.surface.get_rect(center=(self.start_x[random_num], position_y))
        self.movements = 0
        self.alien_movement = BOSS_MOVEMENT
        directions = (1, -1)
        self.direction = directions[random_num]
        self.step_down_amount = 0
        self.anim_iterator = 0
        self.destruct_start_time = None
        self.points = ALIENS_BOSS_POINTS
        pygame.mixer.music.play(loops=-1)

    def move(self):
        """
        Перемещение
        """
        if not self.update_destroyed():
            self.corner.move_ip(self.direction * self.alien_movement, self.step_down_amount)

    def out_of_screen(self):
        """
        Проверка не вышел ли за границы и уничтожение
        """
        if self.corner.right <= 0 or self.corner.left >= SCREEN_WIDTH:
            pygame.mixer.music.stop()
            self.kill()

    def update_destroyed(self):
        """
        Проверка таймера уничтожения, если истекло вызывает уничтожение
        Также смена спрайта уничтожения, еси достигло BOSS_DESTRUCTION_TIME // 3
        """
        if self.destruct_start_time and \
                (pygame.time.get_ticks() - self.destruct_start_time >= BOSS_DESTRUCTION_TIME):
            self.destroy()
            return True

        elif self.destruct_start_time and \
                (pygame.time.get_ticks() - self.destruct_start_time >= BOSS_DESTRUCTION_TIME // 3):
            self.surface = pygame.image.load(ALIEN_BOSS_EXPLOSIONS[1]).convert_alpha().convert_alpha()
            self.surface.set_colorkey(BLACK, pygame.RLEACCEL)

    def init_destruction(self):
        """
        Инициализация уничтожения
        Также смена спрайта уничтожения
        """
        pygame.mixer.music.stop()
        self.surface = pygame.image.load(ALIEN_BOSS_EXPLOSIONS[0]).convert_alpha()
        self.surface.set_colorkey(BLACK, pygame.RLEACCEL)
        self.destruct_start_time = pygame.time.get_ticks()
        self.boss_explosion_sound.play()

    def destroy(self):
        """
        Уничтожения себя
        """
        self.destruct_start_time = None
        self.kill()

