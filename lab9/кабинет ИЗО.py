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


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
x = 400
y = 300
x1 = x - 25
y1 = y - 7

x2 = x - 25
y2 = y + 7

x3 = x + 20
y3 = y + 10

x4 = x + 40
y4 = y + 5

x5 = x + 40
y5 = y

x6 = x + 20
y6 = y - 10


X1 = x - 5
Y1 = y - 40
X2 = x + 15
Y2 = y - 20
X3 = x + 15
Y3 = y + 20
X4 = x - 5
Y4 = y + 40
finished = False

while not finished:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

    screen.fill(WHITE)
    pygame.draw.polygon(screen, [160, 160, 180], [[x1, y1], [x2, y2], [x3, y3], [x4, y4], [x5, y5], [x6, y6]])
    pygame.draw.polygon(screen, [160, 160, 180], [[X1, Y1], [X2, Y2], [X3, Y3], [X4, Y4]])

    pygame.display.update()