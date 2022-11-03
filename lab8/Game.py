import pygame
from pygame.draw import *
from random import randint
import math
pygame.init()


RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]




def number_of_balls():
    '''
    Позволяет выбрать количество одновременно появляющихся шариков на экране и
    генерирует их начальные положения и скорости
    :param number: числр шаров
    '''
    global full_kinematic_data, number_ob
    full_kinematic_data = list()   #Двумерный массив nx5, содержащий информацию о движении всех n шариков на экране
                                   #в порядке x, y, скорость, угол наклона скорости, цвет
    print('Сколько шаров?')
    number_ob = int(input())
    for i in range(number_ob):
        starting_x = randint(100, 1100)
        starting_y = randint(100,900)
        r = randint(30, 60)
        speed = randint(10,20)
        alpha = randint(0, 19) / 20 * math.pi
        color = COLORS[randint(0, 5)]
        full_kinematic_data.append([starting_x, starting_y, r, speed, alpha, color])


def new_ball():
    '''рисует новый шарик '''
    global x, y, r
    x = randint(100, 1100)
    y = randint(100, 900)
    r = randint(10, 100)
    color = COLORS[randint(0, 5)]
    circle(screen, color, (x, y), r)

def mooving_ball(old_x,old_y, r,speed, alpha, color):
    '''
    Рисует новый шарик на месте старого с небольшим смещением
    :param old_x: координата x начального положения шарика
    :param old_y: координата y начального положения шарика
    :param r: радиус шарика
    :param speed: смещение в пикселях за 1 кадр
    :param alpha: угол между осью OX и вектором смещения
    :param color: цвет рисуемого шарика

    kinematic_data: сохраняет данные о положении, скорости и цвете шарика для расчёта
                    следующего его положения
    '''
    global kinematic_data
    new_x = old_x + speed * math.cos(alpha)
    new_y = old_y + speed * math.sin(alpha)
    circle(screen, color, (new_x, new_y), 50)

    kinematic_data = [new_x, new_y, r, speed, alpha, color]

def click(event):
    print(x, y, r)



number_of_balls()


FPS = 30
screen = pygame.display.set_mode((1200, 900))


pygame.display.update()
clock = pygame.time.Clock()
finished = False


while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print('Click!', event.pos)
            click(event)

    #new_ball()
    for i in range(number_ob):
        x, y, r, speed, alpha, color = full_kinematic_data[i]
        mooving_ball(x, y, r, speed, alpha, color)
        full_kinematic_data[i] = kinematic_data


    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()