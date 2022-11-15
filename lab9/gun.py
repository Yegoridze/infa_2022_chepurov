import math
from random import choice
from random import randint
import pygame


FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600
GRAV = 3


class Ball:
    def __init__(self, screen: pygame.Surface, x, y):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy и силы гравитации, действующей на мяч.
        """

        self.x += self.vx
        self.y -= self.vy
        self.vy -= GRAV
        if (self.x + self.r >= WIDTH) and (self.vx > 0):
            self.vx *= -1
        elif (self.x - self.r <= 0) and (self.vx < 0):
            self.vx *= -1
        if (self.y - self.r <= 0) and (self.vy > 0):
            self.vy *= -1

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        len = ((self.x - obj.x) ** 2 + (self.y - obj.y) ** 2) ** 0.5
        hit = 0
        if len < self.r + obj.r:
            hit = 1
        return hit


class Knipel:
    pass


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event and (event.pos[0] > 20) :
            self.an = math.atan((event.pos[1]-450) / (event.pos[0]-20))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        x11 = 40 - 5 * math.sin(self.an)
        y11 = 450 + 5 * math.cos(self.an)
        x12 = 40 + 5 * math.sin(self.an)
        y12 = 450 - 5 * math.cos(self.an)

        x21 = 40 + (self.f2_power + 10) * math.cos(self.an) + 5 * math.sin(self.an)
        y21 = 450 + (self.f2_power + 10) * math.sin(self.an) - 5 * math.cos(self.an)
        x22 = 40 + (self.f2_power + 10) * math.cos(self.an) - 5 * math.sin(self.an)
        y22 = 450 + (self.f2_power + 10) * math.sin(self.an) + 5 * math.cos(self.an)
        pygame.draw.polygon(self.screen, self.color, [[x11, y11], [x12, y12], [x21, y21], [x22, y22]])

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


class Tank():
    def __init__(self, screen):
        self.screen = screen
        self.x = 400
        self.y = 570
        self.f2_power = 10
        self.f2_on = 0
        self.an = 0
        self.color = GREEN
        self.bullet = 1

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event and (event.pos[1] < self.y) :
            self.an = math.atan((event.pos[0]-self.x) / (event.pos[1]-self.y))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY
    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen, self.x, self.y)
        new_ball.r += 5
        if event.pos[1] < self.y:
            self.an = math.atan((event.pos[0]-self.x) / (event.pos[1]-self.y))
        new_ball.vx = - self.f2_power * math.sin(self.an)
        new_ball.vy = self.f2_power * math.cos(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY

    def move(self):
        speed = 0
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[97] and (not (pressed_keys[100])):
            speed = -7
        elif (not (pressed_keys[97])) and pressed_keys[100]:
            speed = 7
        self.x += speed

    def draw(self):
        y11 = self.y + 5 * math.sin(self.an)
        x11 = self.x - 5 * math.cos(self.an)
        y12 = self.y - 5 * math.sin(self.an)
        x12 = self.x + 5 * math.cos(self.an)

        y21 = self.y - (self.f2_power + 20) * math.cos(self.an) - 5 * math.sin(self.an)
        x21 = self.x - (self.f2_power + 20) * math.sin(self.an) + 5 * math.cos(self.an)
        y22 = self.y - (self.f2_power + 20) * math.cos(self.an) + 5 * math.sin(self.an)
        x22 = self.x - (self.f2_power + 20) * math.sin(self.an) - 5 * math.cos(self.an)
        pygame.draw.polygon(self.screen, self.color, [[x11, y11], [x12, y12], [x21, y21], [x22, y22]])
        pygame.draw.circle(self.screen, [29,150,20], [self.x, self.y], 20)
        x1 = self.x - 30
        y1 = self.y
        x2 = self.x - 30
        y2 = self.y + 10
        x3 = self.x - 20
        y3 = self.y + 20
        x4 = self.x + 30
        y4 = self.y
        x5 = self.x + 30
        y5 = self.y + 10
        x6 = self.x + 20
        y6 = self.y + 20
        pygame.draw.polygon(self.screen, [29,100,20], [[x1, y1], [x2, y2], [x3, y3], [x6, y6], [x5, y5], [x4, y4]])
class Target:
    def __init__(self):
        self.screen = screen
        self.points = 0
        self.live = 1
        self.x = 600
        self.y = 300
        self.vx = randint(-5, 5)
        self.vy = randint(-5, 5)
        self.r = 50
        self.color = RED


    def new_target(self):
        """ Инициализация новой цели. """

        self.x = randint(600, 780)
        self.y = randint(300, 550)
        self.r = randint(25, 50)
        self.vx = randint(-5, 5)
        self.vy = randint(-5, 5)
        self.live = 1

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def move(self):
        """Переместить уель по прошествии единицы времени.

        Метод описывает перемещение цели за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy
        """

        self.x += self.vx
        self.y -= self.vy
        if (self.x + self.r >= WIDTH) and (self.vx > 0):
            self.vx *= -1
        elif (self.x - self.r <= 0) and (self.vx < 0):
            self.vx *= -1
        if (self.y + self.r >= HEIGHT - 200) and (self.vy < 0):
            self.vy *= -1
        elif (self.y - self.r <= 0) and (self.vy > 0):
            self.vy *= -1

    def draw(self):
        pygame.draw.circle(self.screen, self.color, [self.x, self.y], self.r)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []

clock = pygame.time.Clock()
gun = Gun(screen)
tank = Tank(screen)

targets = []
for i in range(2):
    targets.append(Target())

finished = False

while not finished:
    screen.fill(WHITE)
    tank.move()
    tank.draw()
    for target in targets:
        target.move()
        target.draw()
    for b in range(len(balls)):
        balls[b].move()
        balls[b].draw()
        balls[b].live += -1
        if balls[b].live == 0:
            del balls[b]

    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            tank.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            tank.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            tank.targetting(event)

    for target in targets:
        for b in balls:

            if b.hittest(target) and target.live:
                target.live = 0
                target.hit()
                target.new_target()
        tank.power_up()

pygame.quit()
