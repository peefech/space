import pygame
from functions import *
from config import *


class Shot(pygame.sprite.Sprite):
    pygame.mixer.init()
    shoot_sound = pygame.mixer.Sound(SHOOT_SOUND)

    def __init__(self, position, speed_bust, shot_width=3, shot_height=20, shot_color=WHITE):
        super().__init__()
        self.surface = pygame.Surface((shot_width, shot_height))
        self.surface.fill(shot_color)

        self.corner = self.surface.get_rect(center=(position[0] + SPACESHIP_WIDTH / 2, position[1]))
        self.direction_x = 0
        self.direction_y = -1
        self.speed = shot_speed(speed_bust)
        self.destruct_start_time = None
        self.shoot_sound.play()

    def move(self):
        """
        Перемещение
        """
        self.corner.move_ip(self.direction_x * self.speed, self.direction_y * self.speed)

    def collision_detect(self, fleet_group, alien_shots, boss_group, scoreboard, bonuses, spaceship):
        """
        Проверка коллизии с разными типами и вызовы методов
        """
        hit = self.fleet_collision(fleet_group, scoreboard)

        self.alien_shot_collision(alien_shots)
        self.boss_collision(boss_group, scoreboard)
        self.bonus_collision(bonuses, spaceship)
        self.out_of_screen()

        return hit

    def fleet_collision(self, fleet_group, scoreboard):
        """
        Проверка коллизии с флотом алиенов
        """
        for alien in fleet_group:
            if alien is not None:
                if self.corner.colliderect(alien.corner):
                    if alien.destruct_start_time is None:
                        self.shoot_sound.stop()
                        alien.init_destruction(fleet_group)
                        scoreboard.increase(alien)
                        self.kill()
                        return True
        return False

    def alien_shot_collision(self, alien_shots):
        """
        Проверка коллизии с пулей алиенов
        """
        for alien_shot in alien_shots:
            if self.corner.colliderect(alien_shot.corner):
                alien_shot.kill()
                self.shoot_sound.stop()
                if self.destruct_start_time is None:
                    self.init_destruction()

    def init_destruction(self, explosion_sprite_path=PLAYER_SHOT_EXPLOSION):
        """
        Инициализация уничтожения
        """
        self.corner = self.surface.get_rect(center=(self.corner[0] - SHOT_EXPLOSION_WIDTH // 2, self.corner[1]))
        self.surface = pygame.image.load(explosion_sprite_path).convert_alpha()
        self.destruct_start_time = pygame.time.get_ticks()

    def boss_collision(self, boss_group, scoreboard):
        """
        Проверка коллизии с боссом
        """
        for boss in boss_group:
            if boss is not None:
                if self.corner.colliderect(boss.corner):
                    if boss.destruct_start_time is None:
                        self.shoot_sound.stop()
                        boss.init_destruction()
                        scoreboard.increase(boss)
                        self.kill()

    def bonus_collision(self, bonuses, spaceship):
        """
        Проверка коллизии с боссом
        """
        for bonus in bonuses:
            if bonus is not None:
                if self.corner.colliderect(bonus.corner):
                    bonus.activate(spaceship)
                    self.kill()

    def out_of_screen(self):
        """
        Проверка за границей ли
        """
        if self.corner.top <= HEIGHT_SCOREBOARD:
            if self.destruct_start_time is None:
                self.shoot_sound.stop()
                self.init_destruction(explosion_sprite_path=PLAYER_SHOT_EXPLOSION_RED)

    def update_destroyed(self):
        """
        Проверка таймера уничтожения
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
