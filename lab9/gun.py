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

SCORE = 0


class Ball:
    def __init__(self, screen: pygame.Surface, x=400, y=100):
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
        global SCORE
        len = ((self.x - obj.x) ** 2 + (self.y - obj.y) ** 2) ** 0.5
        hit = 0
        if len < self.r + obj.r:
            hit = 1
            SCORE += 1
            print(SCORE)
        return hit


class Knipel:
    def __init__(self, screen: pygame.Surface, x, y, an):
        """ Конструктор класса knipel

        Args:
        x - начальное положение книпеля по горизонтали
        y - начальное положение книпеля по вертикали
        l - длина книпеля
        elong - удлиннение за один кадр
        an - угол, на который повернут книпель
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.l = 5
        self.elong = 2
        self.an = an
        self.omega = 0.2
        self.vx = 0
        self.vy = 0
        self.color = BLACK
        self.live = 40

    def move(self):
        """Переместить книпель по прошествии единицы времени.

        Метод описывает перемещение книпеля за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy и силы гравитации, действующей на мяч,
        а также поворачивает книпель на угол self.omega и удлинняет его на self.elong.
        """

        self.x += self.vx
        self.y -= self.vy
        self.vy -= GRAV
        self.an += self.omega
        self.l += self.elong
        if (self.x >= WIDTH) and (self.vx > 0):
            self.vx *= -1
        elif (self.x <= 0) and (self.vx < 0):
            self.vx *= -1
        if (self.y <= 0) and (self.vy > 0):
            self.vy *= -1

    def draw(self):
        x1 = self.x + self.l * math.sin(self.an)
        y1 = self.y + self.l * math.cos(self.an)
        x2 = self.x - self.l * math.sin(self.an)
        y2 = self.y - self.l * math.cos(self.an)
        pygame.draw.line(self.screen, self.color, [x1, y1], [x2, y2], 3)
        pygame.draw.circle(self.screen, self.color, [x1, y1], 3)
        pygame.draw.circle(self.screen, self.color, [x2, y2], 3)

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        global SCORE
        n = 10
        hit = 0
        for i in range(-n, n + 1):
            x = self.x - i * self.l / (2*n) * math.sin(self.an)
            y = self.y - i * self.l / (2*n) * math.cos(self.an)
            len = ((x - obj.x) ** 2 + (y - obj.y) ** 2) ** 0.5

            if len - 1 <= obj.r:
                hit = 1
        if hit == 1:
            SCORE += 1
            print(SCORE)
        return hit


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY

    def fire2_start(self):
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
        if event and (event.pos[0] > 20):
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
        self.bullet_type = 2
        self.live = 1

    def bullet_change(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_1]:
            self.bullet_type = 1
        elif pressed_keys[pygame.K_2]:
            self.bullet_type = 2

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event and (event.pos[1] < self.y):
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
        global balls, knipels, bullet
        if self.bullet_type == 1:
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
        else:
            bullet += 1
            new_knipel = Knipel(self.screen, self.x, self.y, self.an)
            if event.pos[1] < self.y:
                self.an = math.atan((event.pos[0] - self.x) / (event.pos[1] - self.y))
            new_knipel.vx = - self.f2_power * math.sin(self.an)
            new_knipel.vy = self.f2_power * math.cos(self.an)
            knipels.append(new_knipel)
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
        if pressed_keys[97] and (not (pressed_keys[100])) and self.x > 20:
            speed = -7
        elif (not (pressed_keys[97])) and pressed_keys[100] and self.x < WIDTH - 20:
            speed = 7
        self.x += speed

    def tank_hittest(self, obj):
        """Функция проверяет сталкивалкивается ли танк с целью (бомбой), описываемой в обьекте obj,
        и если столконвение происходит, уменьшает жизни танка до 0.
        Args:
            obj: Обьект, с которым проверяется столкновение.
        """
        global SCORE
        x1 = self.x + 30
        y1 = self.y
        x2 = self.x + 30
        y2 = self.y + 20
        x3 = self.x - 30
        y3 = self.y + 20
        x4 = self.x - 30
        y4 = self.y
        x5 = self.x - 15
        y5 = self.y - 20
        x6 = self.x + 15
        y6 = self.y - 20
        dots = [[x1, y1], [x2, y2], [x3, y3], [x4, y4], [x5, y5], [x6, y6]]
        for dot in dots:
            len = ((dot[0] - obj.x) ** 2 + (dot[1] - obj.y) ** 2) ** 0.5
            if len <= obj.r:
                self.live = 0

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
        pygame.draw.circle(self.screen, [29, 150, 20], [self.x, self.y], 20)
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
        pygame.draw.polygon(self.screen, [29, 100, 20], [[x1, y1], [x2, y2], [x3, y3], [x6, y6], [x5, y5], [x4, y4]])


class Target:
    def __init__(self):
        self.screen = screen
        self.points = 0
        self.live = 1
        self.x = randint(100, 700)
        self.y = randint(100, 400)
        self.vx = randint(-5, 5)
        self.vy = randint(-5, 5)
        self.r = 50
        self.color = RED

    def new_target(self):
        """ Инициализация новой цели. """

        self.x = randint(100, 700)
        self.y = randint(100, 400)
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


class Bomb(Ball):
    """
    Класс бомб. Обладает горизонтальными и вертикальными координатами и скоростями x, y и vx, xy.
    Экземпляры создаются самолётом и падают по вертикали. При достижении определённой y-координаты,
    увеличивается в размерах, "взрываясь". При соприкосновении с танком срабатывает
    функция танка, обнулябщая его жизни.
    """
    def __init__(self, screen: pygame.Surface, x, y):
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 15
        self.vx = 0
        self.vy = 0
        self.color = BLACK
        self.live = 30

    def move(self):
        """
        Переместить бомбу по прошествии единицы времени с учётом гравитации.
        Метод описывает перемещение мяча за один кадр перерисовки.
        """
        self.y -= self.vy
        self.vy -= GRAV
        if self.y >= 540:
            self.r = 40
            self.color = RED
            self.vy -= 80

    def draw(self):
        """Рисует круглую бомбу радиусом self.r"""
        pygame.draw.circle(self.screen, self.color,
                           [self.x, self.y], self.r
                           )


class F117(Target):
    def __init__(self):
        self.screen = screen
        self.points = 0
        self.live = 1
        self.x = randint(100, 700)
        self.y = randint(100, 300)
        self.vx = randint(-5, 5)
        self.vy = 0
        self.r = 35
        self.color = [160, 160, 180]
        self.bomb_reload = 0

    def new_plane(self):
        """ Инициализация новой цели. """

        self.x = randint(100, 700)
        self.y = randint(100, 400)
        self.r = randint(25, 50)
        self.vx = randint(-5, 5)
        self.vy = 0
        self.live = 1

    def bombing(self):
        print('вжжжжжуууууууууууБАМ')
        return Bomb(self.screen, self.x, self.y)

    def draw(self):
        x1 = self.x - 25
        y1 = self.y - 7
        x2 = self.x - 25
        y2 = self.y + 7
        x3 = self.x + 20
        y3 = self.y + 10
        x4 = self.x + 40
        y4 = self.y + 5
        x5 = self.x + 40
        y5 = self.y
        x6 = self.x + 20
        y6 = self.y - 10

        X1 = self.x - 5
        Y1 = self.y - 40
        X2 = self.x + 15
        Y2 = self.y - 20
        X3 = self.x + 15
        Y3 = self.y + 20
        X4 = self.x - 5
        Y4 = self.y + 40
        pygame.draw.polygon(screen, [160, 160, 180], [[x1, y1], [x2, y2], [x3, y3], [x4, y4], [x5, y5], [x6, y6]])
        pygame.draw.polygon(screen, [160, 160, 180], [[X1, Y1], [X2, Y2], [X3, Y3], [X4, Y4]])


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []
knipels = []

clock = pygame.time.Clock()
gun = Gun(screen)
tank = Tank(screen)

targets = []
planes = []
bombs = []
for i in range(2):
    targets.append(Target())
for i in range(1):
    planes.append(F117())

finished = False

while not finished:
    if tank.live == 0:
        finished = True
    screen.fill(WHITE)
    tank.move()
    tank.draw()
    tank.bullet_change()

    for target in targets:
        target.move()
        target.draw()
    for plane in planes:
        plane.move()
        plane.draw()
        if plane.bomb_reload + randint(-60, 60) >= 200:
            plane.bomb_reload = 0
            bombs.append(plane.bombing())
        else:
            plane.bomb_reload += 1

    for b in range(len(balls) - 1, -1, -1):
        balls[b].move()
        balls[b].draw()
        balls[b].live += -1
        if balls[b].live == 0:
            del balls[b]

    for k in range(len(knipels) - 1, -1, -1):
        knipels[k].move()
        knipels[k].draw()
        knipels[k].live += -1
        if knipels[k].live == 0:
            del knipels[k]

    for b in range(len(bombs) - 1, -1, -1):
        bombs[b].move()
        bombs[b].draw()
        bombs[b].live += -1
        if bombs[b].live == 0:
            del bombs[b]

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
        for k in knipels:
            if k.hittest(target) and target.live:
                target.live = 0
                target.hit()
                target.new_target()

        for plane in planes:
            for b in balls:
                if b.hittest(plane) and plane.live:
                    plane.live = 0
                    plane.hit()
                    plane.new_target()
            for k in knipels:
                if k.hittest(plane) and target.live:
                    plane.live = 0
                    plane.hit()
                    plane.new_plane()

        for bomb in bombs:
            tank.tank_hittest(bomb)
        tank.power_up()

print('\nGame over! \nНабрано очков:', SCORE)
pygame.quit()
