import pygame
import random
import sys
from pygame.locals import *

# Инициализация Pygame
pygame.init()

# Настройки экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pacman Game")

# Цвета
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Частота кадров
FPS = 60
clock = pygame.time.Clock()


class Background:
    def __init__(self):
        self.image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.image.fill(BLUE)
        # Добавим сетку для фона
        for x in range(0, SCREEN_WIDTH, 20):
            pygame.draw.line(self.image, BLACK, (x, 0), (x, SCREEN_HEIGHT), 1)
        for y in range(0, SCREEN_HEIGHT, 20):
            pygame.draw.line(self.image, BLACK, (0, y), (SCREEN_WIDTH, y), 1)

    def draw(self, surface):
        surface.blit(self.image, (0, 0))


class Pacman:
    def __init__(self):
        self.radius = 20
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.speed = 5
        self.direction = 0  # 0: right, 1: left, 2: up, 3: down
        self.mouth_angle = 0
        self.mouth_change = 5
        self.max_mouth_angle = 45
        self.mouth_open = True
        self.moving = False

    def update(self):
        # Движение
        if self.moving:
            if self.direction == 0 and self.x < SCREEN_WIDTH - self.radius:
                self.x += self.speed
            elif self.direction == 1 and self.x > self.radius:
                self.x -= self.speed
            elif self.direction == 2 and self.y > self.radius:
                self.y -= self.speed
            elif self.direction == 3 and self.y < SCREEN_HEIGHT - self.radius:
                self.y += self.speed

            # Анимация рта
            if self.mouth_open:
                self.mouth_angle += self.mouth_change
                if self.mouth_angle >= self.max_mouth_angle:
                    self.mouth_open = False
            else:
                self.mouth_angle -= self.mouth_change
                if self.mouth_angle <= 0:
                    self.mouth_open = True
        else:
            # Если не двигается, рот должен быть закрыт
            self.mouth_angle = 0

    def draw(self, surface):
        # Рисуем Pacman
        if self.mouth_angle == 0:  # Если рот закрыт - просто круг
            pygame.draw.circle(surface, YELLOW, (self.x, self.y), self.radius)
        else:
            # Углы для дуги (в радианах)
            if self.direction == 0:  # right
                start_angle = self.mouth_angle * 3.14 / 180
                end_angle = (360 - self.mouth_angle) * 3.14 / 180
            elif self.direction == 1:  # left
                start_angle = (180 + self.mouth_angle) * 3.14 / 180
                end_angle = (180 - self.mouth_angle) * 3.14 / 180
            elif self.direction == 2:  # up
                start_angle = (270 + self.mouth_angle) * 3.14 / 180
                end_angle = (270 - self.mouth_angle) * 3.14 / 180
            elif self.direction == 3:  # down
                start_angle = (90 + self.mouth_angle) * 3.14 / 180
                end_angle = (90 - self.mouth_angle) * 3.14 / 180

            # Точки для линий рта
            points = []
            points.append((self.x, self.y))  # Центр

            # Первая точка рта
            if self.direction == 0:  # right
                points.append((self.x + self.radius, self.y - self.mouth_angle / 2))
            elif self.direction == 1:  # left
                points.append((self.x - self.radius, self.y - self.mouth_angle / 2))
            elif self.direction == 2:  # up
                points.append((self.x - self.mouth_angle / 2, self.y - self.radius))
            elif self.direction == 3:  # down
                points.append((self.x - self.mouth_angle / 2, self.y + self.radius))

            # Вторая точка рта
            if self.direction == 0:  # right
                points.append((self.x + self.radius, self.y + self.mouth_angle / 2))
            elif self.direction == 1:  # left
                points.append((self.x - self.radius, self.y + self.mouth_angle / 2))
            elif self.direction == 2:  # up
                points.append((self.x + self.mouth_angle / 2, self.y - self.radius))
            elif self.direction == 3:  # down
                points.append((self.x + self.mouth_angle / 2, self.y + self.radius))

            # Рисуем заполненный сектор
            pygame.draw.polygon(surface, YELLOW, points)
            pygame.draw.arc(surface, BLACK,
                            (self.x - self.radius, self.y - self.radius,
                             self.radius * 2, self.radius * 2),
                            start_angle, end_angle, 2)

        # Глаз
        eye_offset_x, eye_offset_y = 0, 0
        if self.direction == 0:
            eye_offset_x = 5
        elif self.direction == 1:
            eye_offset_x = -5
        elif self.direction == 2:
            eye_offset_y = -5
        elif self.direction == 3:
            eye_offset_y = 5

        pygame.draw.circle(surface, BLACK,
                           (self.x + eye_offset_x, self.y + eye_offset_y - 5), 5)


class Enemy:
    def __init__(self):
        self.radius = 15
        self.x = random.randint(self.radius, SCREEN_WIDTH - self.radius)
        self.y = random.randint(self.radius, SCREEN_HEIGHT - self.radius)
        self.speed = 3
        self.direction = random.randint(0, 3)  # 0: right, 1: left, 2: up, 3: down
        self.direction_time = 0
        self.change_direction_time = 5000  # 5 секунд в миллисекундах
        self.active = True

    def update(self, current_time):
        if not self.active:
            return

        # Меняем направление каждые 5 секунд
        if current_time - self.direction_time > self.change_direction_time:
            self.direction = random.randint(0, 3)
            self.direction_time = current_time

        # Движение
        if self.direction == 0:  # right
            self.x += self.speed
            if self.x > SCREEN_WIDTH - self.radius:
                self.x = SCREEN_WIDTH - self.radius
                self.direction = random.choice([1, 2, 3])
        elif self.direction == 1:  # left
            self.x -= self.speed
            if self.x < self.radius:
                self.x = self.radius
                self.direction = random.choice([0, 2, 3])
        elif self.direction == 2:  # up
            self.y -= self.speed
            if self.y < self.radius:
                self.y = self.radius
                self.direction = random.choice([0, 1, 3])
        elif self.direction == 3:  # down
            self.y += self.speed
            if self.y > SCREEN_HEIGHT - self.radius:
                self.y = SCREEN_HEIGHT - self.radius
                self.direction = random.choice([0, 1, 2])

    def draw(self, surface):
        if self.active:
            pygame.draw.circle(surface, RED, (self.x, self.y), self.radius)
            # Глаза врага
            pygame.draw.circle(surface, BLACK, (self.x - 5, self.y - 5), 3)
            pygame.draw.circle(surface, BLACK, (self.x + 5, self.y - 5), 3)


class Game:
    def __init__(self):
        self.background = Background()
        self.pacman = Pacman()
        self.enemies = [Enemy() for _ in range(4)]
        self.score = 0
        self.font = pygame.font.SysFont(None, 36)
        self.game_time = pygame.time.get_ticks()

    def quit_game(self):
        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.quit_game()

            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    self.pacman.direction = 1
                    self.pacman.moving = True
                elif event.key == K_RIGHT:
                    self.pacman.direction = 0
                    self.pacman.moving = True
                elif event.key == K_UP:
                    self.pacman.direction = 2
                    self.pacman.moving = True
                elif event.key == K_DOWN:
                    self.pacman.direction = 3
                    self.pacman.moving = True
                elif event.key == K_ESCAPE:  # выход по ESC
                    self.quit_game()

            if event.type == KEYUP:
                if event.key in [K_LEFT, K_RIGHT, K_UP, K_DOWN]:
                    self.pacman.moving = False

    def update(self):
        current_time = pygame.time.get_ticks()
        self.pacman.update()

        for enemy in self.enemies:
            enemy.update(current_time)

            # Проверка столкновения с Pacman
            if enemy.active:
                distance = ((self.pacman.x - enemy.x) ** 2 +
                            (self.pacman.y - enemy.y) ** 2) ** 0.5
                if distance < self.pacman.radius + enemy.radius:
                    enemy.active = False
                    self.score += 1

        # Если все враги съедены, создаем новых
        if all(not enemy.active for enemy in self.enemies):
            self.enemies = [Enemy() for _ in range(4)]

    def draw(self):
        self.background.draw(screen)
        self.pacman.draw(screen)

        for enemy in self.enemies:
            enemy.draw(screen)

        # Отображаем счет
        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        screen.blit(score_text, (10, 10))

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.update()
            clock.tick(FPS)


# Запуск игры
if __name__ == "__main__":
    game = Game()
    game.run()