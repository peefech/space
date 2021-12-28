from config import *
import json
import pygame


class Scoreboard:
    def __init__(self):
        self.hi_score = 0

        self.load_hi_score()
        self.score = 0
        self.lives = LIVES
        self.font = pygame.font.SysFont("Consolas", 25, bold=False)

        self.green_line = []

    def load_hi_score(self):
        """
        Загрузка hi-score
        """

        with open(HI_SCORE_PATH, "r") as file:
            data = json.load(file)
        self.hi_score = data["hi-score"]

    def write_hi_score(self):
        """
        Запись (нового) рекорда в файл
        """
        self.update_hi_score()
        data = {
            "hi-score": self.hi_score
        }
        with open(HI_SCORE_PATH, "w") as file:
            json.dump(data, file)

    def update_hi_score(self):
        """
        Обновление рекорда
        """
        if self.score > self.hi_score:
            self.hi_score = self.score

    def build_hud_line(self):
        """
        Строит нижнюю зеленую линюю
        """
        for i in range(SCREEN_WIDTH // GREEN_LINE_SIZE + 1):
            pixel = pygame.Surface((GREEN_LINE_SIZE, GREEN_LINE_SIZE))
            pixel.fill(GREEN)
            corner = pixel.get_rect(center=(i * GREEN_LINE_SIZE, SCREEN_HEIGHT - 70))
            dictionary = {
                "pixel": pixel,
                "corner": corner
            }
            self.green_line.append(dictionary)

    def increase(self, alien):
        """
        Прибавление очков за уничтожение
        """
        self.score += alien.points

    def remove_life(self):
        """
        Минус одна жизнь корабля
        """
        if self.lives > 0:
            self.lives -= 1
