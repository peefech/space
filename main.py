import pygame
import time

from config import *
from spaceship import SpaceShip
from scoreboard import Scoreboard
from functions import *
from random import choice
from boss import Boss
from alien_shot import AlienShot
from shot import Shot


class Game:

    def __init__(self):

        global screen, scoreboard, spaceship

        pygame.init()

        screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

        scoreboard = Scoreboard()

        spaceship = SpaceShip()

        self.font = pygame.font.Font("fonts/prstart.ttf", 30)

    def drawIntroScreen(self):
        """
        Нарисовать интро скрин
        """

        global screen, scoreboard, spaceship

        screen.fill([0, 0, 0])

        if pygame.font.get_init():
            hi_score = scoreboard.hi_score

            write_on_screen("SCORE<1>", "white", [50, 30], screen, self.font)
            write_on_screen("HI-SCORE", "white", [350, 30], screen, self.font)

            write_on_screen("0", "white", [110, 90], screen, self.font)
            write_on_screen(str(hi_score), "white", [450, 90], screen, self.font)

            write_one_symbol("PLAY", [400, 190], 100, screen, self.font)

            write_one_symbol("SPACE   INVADERS", [220, 290], 100, screen, self.font)

            write_on_screen("*SCORE ADVANCE TABLE*", "white", [140, 410], screen, self.font)

            picture_score(screen)

            write_one_symbol("=? MYSTERY", [370, 500], 100, screen, self.font)
            write_one_symbol("=30 POINTS", [370, 580], 100, screen, self.font)
            write_one_symbol("=20 POINTS", [370, 660], 100, screen, self.font)
            write_one_symbol("=10 POINTS     ", [370, 740], 100, screen, self.font)

            stage_loop()

            screen.fill([0, 0, 0])

            write_on_screen("SCORE<1>", "white", [50, 30], screen, self.font)
            write_on_screen("HI-SCORE", "white", [350, 30], screen, self.font)

            write_on_screen("0", "white", [110, 90], screen, self.font)
            write_on_screen(str(hi_score), "white", [450, 90], screen, self.font)

            write_on_screen("PLAY PLAYER <1>", "white", [250, 410], screen, self.font)
            write_on_screen(f"{spaceship.lives}     ", "white", [140, 962], screen, self.font)

            life_icon = pygame.image.load(SPACESHIP_PATH).convert_alpha()
            life_icon.set_colorkey(BLACK, pygame.RLEACCEL)

            for j in range(1, scoreboard.lives + 1):
                life_corner = life_icon.get_rect(center=(150 + j * 60, SCREEN_HEIGHT - 35))
                screen.blit(life_icon, life_corner)

            pygame.display.flip()

        stage_loop()

    def next_level(self, lives=3, score=0, movement=MOVEMENT_DELAY):
        """
        Старт следующего уровня, в том числе 1
        """
        global screen, scoreboard, spaceship

        alien_move_sounds = (pygame.mixer.Sound(ALIEN_MOVEMENT_SOUND_1), pygame.mixer.Sound(ALIEN_MOVEMENT_SOUND_2),
                             pygame.mixer.Sound(ALIEN_MOVEMENT_SOUND_3), pygame.mixer.Sound(ALIEN_MOVEMENT_SOUND_4))

        game_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        game_surface.fill([0, 0, 0])

        spaceship.lives = lives
        scoreboard.score = score

        shots = pygame.sprite.Group()

        alien_shots = pygame.sprite.Group()

        fleet_group = []

        alien_count = create_alien_fleet(fleet_group)

        boss_group = pygame.sprite.Group()

        # Игровой круг

        clock = pygame.time.Clock()
        game_on = True
        boss_time = time.time()
        movement_time = time.time()
        movement_sound_time = time.time()
        shoot_time = time.time()
        movement_delay = movement
        movement_sound_delay = movement_delay + MOVEMENT_SOUND_DELAY
        movement_sound_counter = 0
        i = 0
        life_icon = pygame.image.load(SPACESHIP_PATH).convert_alpha()
        life_icon.set_colorkey(BLACK, pygame.RLEACCEL)
        out_of_screen = False
        turned_counter = 0
        out_of_bounds = False

        while game_on:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_on = quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_on = quit()

            # Коллизия пуль с игроками и врагами

            for shot in shots:
                if shot.destruct_start_time is None:
                    shot.move()
                    hit = shot.collision_detect(fleet_group, alien_shots, boss_group, scoreboard)

                    if hit:
                        alien_count -= 1
                else:
                    shot.update_destroyed()

            pressed_keys = pygame.key.get_pressed()

            if spaceship.destruct_start_time is None and spaceship.control(pressed_keys):
                shots.add(Shot(position=spaceship.corner))

            if spaceship.destruct_start_time is not None:
                spaceship.update_destroyed()

            # Перемещение врагов и стрельба

            if time.time() - shoot_time > ALIEN_SHOOT_DELAY:
                while True:
                    shoot_time = time.time()
                    random_alien = choice(fleet_group)
                    if random_alien is None:
                        continue
                    # вычисление местоположения алиена
                    # перед выбранным алиеном не должно быть других
                    # вычисляем позицию снизу этого алиена и если он существует
                    # то берем другого
                    can_shoot = True
                    for j in range(random_alien.row + 1, ROWS):
                        position = j * COLUMNS + random_alien.column
                        if fleet_group[position] is not None:
                            can_shoot = False
                            break
                    if can_shoot:
                        break

                alien_shots.add(AlienShot(random_alien.corner))

            for alien_shot in alien_shots:
                if alien_shot.destruct_start_time is None:
                    alien_shot.move()
                    alien_shot.collision_detect(scoreboard.green_line, spaceship, scoreboard)
                else:
                    alien_shot.update_destroyed()

            if time.time() - movement_sound_time > movement_sound_delay:
                movement_sound_time = time.time()
                alien_move_sounds[movement_sound_counter].play()
                if movement_sound_counter < len(alien_move_sounds) - 1:
                    movement_sound_counter += 1
                else:
                    movement_sound_counter = 0

            # передвижение алиенов интервалами
            if time.time() - movement_time > movement_delay:
                movement_time = time.time()

                if turned_counter == 0:
                    out_of_bounds = False
                    for alien in fleet_group:
                        if alien is not None:
                            alien.update_destroyed()

                        if alien is not None and (alien.corner.left <= 40 or alien.corner.right >= SCREEN_WIDTH - 40):
                            column_crossed = alien.column
                            out_of_bounds = True
                            # также проверяем у всех алиенов в этом столбце как у них дела (вышли ли за границы),
                            # чтобы было все синхронно
                            for another_alien in fleet_group:
                                if another_alien is not None and another_alien.column == column_crossed:
                                    if another_alien.corner.left > 40 and \
                                            another_alien.corner.right < SCREEN_WIDTH - 40:
                                        out_of_bounds = False
                                        break
                            break

                for alien in fleet_group:
                    if alien is not None:
                        if alien.row == ROWS - i:
                            # если ВСЕ алиены в столбце пересекли границу, тогда меняем так уж и быть напрвление
                            if out_of_bounds and turned_counter <= ROWS:
                                alien.direction *= -1
                                alien.step_down()
                            alien.move()
                            out_of_screen = alien.out_of_screen()

                if out_of_bounds and turned_counter <= ROWS:
                    turned_counter += 1
                else:
                    turned_counter = 0

                # ищем кол-во уничтоженных полностью слотбцов
                missing_columns = 0

                for j in range(COLUMNS):
                    alien_is_live = False
                    for alien in fleet_group:
                        if alien is not None and alien.column == j:
                            alien_is_live = True
                            break
                    if not alien_is_live:
                        missing_columns += 1

                movement_delay = MOVEMENT_DELAY - (missing_columns * (MOVEMENT_DELAY / (COLUMNS - 1)))

                movement_sound_delay = MOVEMENT_SOUND_DELAY - (
                        missing_columns * (MOVEMENT_SOUND_DELAY / 1.3 / (COLUMNS - 1)))

                if i < ROWS:
                    i += 1
                else:
                    i = 0
            else:
                for alien in fleet_group:
                    if alien is not None:
                        alien.update_destroyed()

            if time.time() - boss_time > BOSS_APPEARANCE_DELAY:
                boss_time = time.time()
                boss_group.add(Boss())
            for boss in boss_group:
                if boss is not None:
                    if boss.destruct_start_time is None:
                        boss.move()
                        boss.out_of_screen()
                    else:
                        boss.update_destroyed()

            # Рендер

            screen.blit(game_surface, (0, 0))

            for alien in fleet_group:
                if alien is not None:
                    screen.blit(alien.surface, alien.corner)

            for boss in boss_group:
                if boss is not None:
                    screen.blit(boss.surface, boss.corner)

            if spaceship.surface is not None:
                screen.blit(spaceship.surface, spaceship.corner)

            for shot in shots:
                screen.blit(shot.surface, shot.corner)

            for shot in alien_shots:
                screen.blit(shot.surface, shot.corner)

            write_on_screen(f"SCORE<1>", "white", [50, 30], screen, self.font)
            write_on_screen(f"HI-SCORE", "white", [350, 30], screen, self.font)

            write_on_screen(str(scoreboard.score), "white", [110, 90], screen, self.font)
            write_on_screen(str(scoreboard.hi_score), "white", [450, 90], screen, self.font)

            write_on_screen(f"{spaceship.lives}            ", "white", [140, 962], screen, self.font)

            for pixel in scoreboard.green_line:
                if pixel is not None:
                    screen.blit(pixel["pixel"], pixel["corner"])

            for j in range(1, spaceship.lives + 1):
                life_corner = life_icon.get_rect(center=(150 + j * 60, SCREEN_HEIGHT - 35))
                screen.blit(life_icon, life_corner)

            # Рендер итога

            # если игрок победил
            if alien_count == 0:
                pygame.mixer.music.stop()
                # Подождать (2) секунды до конца
                pygame.time.delay(END_SCREEN_TIME // 2)
                # вызов следующего уровня
                self.next_level(spaceship.lives + 1, scoreboard.score, MOVEMENT_DELAY / 1.2)

            # если игрок проиграл
            if spaceship.lives == 0 or out_of_screen:
                pygame.mixer.music.stop()

                write_on_screen("GAME OVER", "red", [340, 450], screen, self.font)
                pygame.display.flip()

                if scoreboard.score > scoreboard.hi_score:

                    # да костыли, но работает же
                    write_on_screen(str(scoreboard.hi_score), "black", [450, 90], screen, self.font)

                    scoreboard.write_hi_score()

                    write_on_screen(str(scoreboard.hi_score), "white", [450, 90], screen, self.font)

                    pygame.display.update()

                # Подождать (5) секунд до конца
                pygame.time.delay(END_SCREEN_TIME)
                game_on = False

            pygame.display.flip()

            # Установка обновления (60 фпс)
            clock.tick(60)

        self.drawIntroScreen()
        self.next_level()


if __name__ == "__main__":
    game = Game()
    game.drawIntroScreen()
    game.next_level()
