import pygame
from config import *
import random


class AlienShot(pygame.sprite.Sprite):

    pygame.mixer.init()
    player_explosion_sound = pygame.mixer.Sound(PLAYER_EXPLOSION_SOUND)

    def __init__(self, position):
        super().__init__()

        paths = random.choice((ALIEN_SHOT_PATHS, ALIEN_SHOT_2_PATHS, ALIEN_SHOT_3_PATHS))
        self.sprites = []
        for path in paths:
            self.sprites.append(pygame.image.load(path).convert_alpha())

        self.current = 0
        self.surface = self.sprites[self.current]
        self.surface.set_colorkey(BLACK, pygame.RLEACCEL)
        self.corner = self.surface.get_rect(center=(position[0] + SPACESHIP_WIDTH / 2, position[1]))
        self.direction_x = 0
        self.direction_y = 1
        self.speed = ALIEN_SHOT_SPEED
        self.update_count = 0
        self.destruct_start_time = None

    def move(self):
        """
        Передвижение пули
        """
        self.update()
        self.corner.move_ip(self.direction_x * self.speed, self.direction_y * self.speed)

    def update(self):
        """
        Анимация пули
        """
        if self.update_count % ALIEN_SHOT_UPDATE_SPEED == 0:
            if self.current < len(self.sprites) - 1:
                self.current += 1
            else:
                self.current = 0

            self.surface = self.sprites[self.current]
            self.surface.set_colorkey(BLACK, pygame.RLEACCEL)
            self.update_count = 0
        self.update_count += 1

    def collision_detect(self, green_line, spaceship, scoreboard):
        """
        Обработка коллизий с разными типами, возвращает Тру, если было попадание в корабль
        """
        self.out_of_screen()
        self.line_collision(green_line)
        if spaceship is not None and self.spaceship_collision(spaceship, scoreboard):
            return True
        return False

    def out_of_screen(self):
        """
        Инициалазция уничтожения, если вышло за экран
        """
        if SCREEN_HEIGHT + ALIEN_SHOT_EXPLOSION_HEIGHT // 2 <= self.corner.bottom:
            if self.destruct_start_time is None:
                self.init_destruction(explosion_sprite=ALIEN_SHOT_EXPLOSION_GREEN)

    def line_collision(self, green_line):
        """
        Проверка колизии с линией и ее уничтожение по пикселям
        """
        for i in range(len(green_line)):
            if green_line[i] is not None:
                if self.corner.colliderect(green_line[i]["corner"]) and self.destruct_start_time is None:
                    self.init_destruction(explosion_sprite=ALIEN_SHOT_EXPLOSION_GREEN)
                    green_line[i] = None

    def spaceship_collision(self, spaceship, scoreboard):
        """
        Инициалазция уничтожения корабля игрока, если было попадание
        """
        if self.corner.colliderect(spaceship.corner) and spaceship.destruct_start_time is None:
            if self.destruct_start_time is None:
                self.init_destruction()
                if not spaceship.sheet:
                    self.player_explosion_sound.play()
                    scoreboard.remove_life()
                    spaceship.remove_life()
                    return True
        return False

    def init_destruction(self, explosion_sprite=ALIEN_SHOT_EXPLOSION):
        """
        Инициалазция уничтожения, путем подмены спрайта
        """
        self.surface = pygame.image.load(explosion_sprite).convert_alpha()
        self.destruct_start_time = pygame.time.get_ticks()

    def update_destroyed(self):
        """
        Проверка, не истекло ли время уничтожения
        """
        if self.destruct_start_time and (pygame.time.get_ticks() - self.destruct_start_time >= DESTRUCTION_TIME):
            self.destroy()
            return True
        return False

    def destroy(self):
        """
        Уничтожение
        """
        self.destruct_start_time = None
        self.kill()
