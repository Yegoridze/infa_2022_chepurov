import pygame
from pygame.draw import *
from random import randint
import math
pygame.init()


SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 700

R_MAX = 30
R_MIN = 20
SP_MAX = 10
SP_MIN = 5
A_MAX = 50
A_MIN = 10


SCORE = 0
TRIES = 0


RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]


def number_of_balls():
    """
    Позволяет выбрать количество одновременно появляющихся шариков на экране и
    генерирует их начальные положения, радиусы и векторные скорости
    :return [number_of_b, full_kin_data] число появляющихся шариков и
    случайный массив nx5, где n - число шариков, а в каждой строке записаны
    x, y, r, скорость, угол наклона скорости, цвет одного из шариков
    """
    full_kinematic_data = list()
    print('Сколько шаров?')
    number_of_b = int(input())
    for j in range(number_of_b):
        starting_x = randint(R_MAX, SCREEN_WIDTH - R_MAX)
        starting_y = randint(R_MAX, SCREEN_HEIGHT - R_MAX)
        generated_r = randint(R_MIN, R_MAX)
        generated_speed = randint(SP_MIN, SP_MAX)
        starting_alpha = randint(0, 19) * math.pi / 10
        generated_color = COLORS[randint(0, 5)]
        full_kinematic_data.append(
                                   [starting_x, starting_y, generated_r,
                                    generated_speed, starting_alpha, generated_color]
                                  )
    return [number_of_b, full_kinematic_data]


def number_of_trolls():
    """
    Позволяет выбрать количество одновременно появляющихся квадратов на экране и
    генерирует их начальные положения, размеры, скорости и их изменения за 1 кадр
    Квадраты линейно меняют свои размеры и модуль скорости в заданных пределах
    :return [number_tr, full_kin_data_troll] число появляющихся квадратов и
    случайный массив nx5, где n - число квадратов, а в каждой строке записаны
    x, y, a, скорость изменения a, скорость, ускорение, угол наклона скорости, цвет
    """
    full_kinematic_data_troll = list()   # Массив nx5, содержащий информацию о движении всех n квадратов на экране
                                   
    print('Сколько квадратов?')
    number_of_tr = int(input())
    for j in range(number_of_tr):
        starting_x = randint(A_MAX, SCREEN_WIDTH - A_MAX)
        starting_y = randint(A_MAX, SCREEN_HEIGHT - A_MAX)
        starting_a = randint(A_MIN, A_MAX)
        starting_diff_a = randint(1, 4)
        starting_speed = randint(SP_MIN, SP_MAX)
        starting_accel = randint(1, 4)
        starting_alpha = randint(0, 19) * math.pi / 10
        generated_color = COLORS[randint(0, 5)]
        full_kinematic_data_troll.append(
                                   [starting_x, starting_y, starting_a, starting_diff_a,
                                    starting_speed, starting_accel, starting_alpha, generated_color]
                                  )
    return [number_of_tr, full_kinematic_data_troll]


def troll_figure(x_center, y_center, side, const_color):
    """
    Рисует квадрат с центром в точке (x_center, y_center), сторонами a
    цвета const_color (в формате, подходящем для pygame.Color)
    """
    x_left_up = int(x_center - side / 2)
    y_left_up = int(y_center - side / 2)
    rect(
         screen, const_color,
         (x_left_up, y_left_up, side, side)
        )


def mooving_troll_figure(
                         old_x, old_y, old_a, const_diff_a,
                         ch_speed, ch_accel, ch_alpha, const_color
                        ):
    """
    Принимает на вход данные о кинематике и цвете квадрата и
    рисует новый квадрат на масте старого с учётом смещения.
    Итоговое изображение движется с постоянным ускорением,
    меняющим направление при достижении скоростью одной из границ
    :param old_x: x-координата начального положения квадрата
    :param old_y: y-координата начального положения квадрата
    :param old_a: начальная длина стороны квадрата
    :param const_diff_a: изменение a за 1 кадр ( >0 при увеличении a, <0 при уменьшении
    :param ch_speed: начальная скорость квадрата
    :param ch_accel: ускорение квадрата
    :param ch_alpha: угол между скоростью и осью OX
    :param const_color: цвет квадрата в формате, подходящем для pygame.Color
    :return:
    """
    ch_alpha = if_hit_the_wall(old_x, old_y, a, ch_alpha)
    if (ch_speed >= SP_MAX) or (ch_speed <= -SP_MIN):
        ch_accel = - ch_accel
    new_x = old_x + ch_speed * math.cos(ch_alpha)
    new_y = old_y + ch_speed * math.sin(ch_alpha)
    if (a >= A_MAX) or (a <= A_MIN):
        const_diff_a = - const_diff_a
    new_a = old_a + const_diff_a
    ch_speed += accel
    troll_figure(new_x, new_y, new_a, const_color)
    kinematic_data_troll = [new_x, new_y, new_a, const_diff_a,
                            ch_speed, ch_accel, ch_alpha, const_color]
    return kinematic_data_troll


def mooving_ball(old_x, old_y, const_r, const_speed, old_alpha, const_color):
    """
    Рисует новый шарик на месте старого с небольшим смещением
    :param old_x: координата x начального положения шарика
    :param old_y: координата y начального положения шарика
    :param const_r: радиус шарика
    :param const_speed: смещение в пикселях за 1 кадр
    :param old_alpha: угол между осью OX и вектором смещения
    :param const_color: цвет рисуемого шарика
    kin_data: сохраняет данные о положении, скорости и цвете шарика для расчёта
                    следующего его положения
    """
    new_alpha = if_hit_the_wall(old_x, old_y, const_r, old_alpha)
    new_x = old_x + const_speed * math.cos(new_alpha)
    new_y = old_y + const_speed * math.sin(new_alpha)
    circle(screen, const_color, (new_x, new_y), const_r)
    kinematic_data = [new_x, new_y, const_r,
                      const_speed, new_alpha, const_color]
    return kinematic_data


def if_hit_the_wall(current_x, current_y, ball_r, changing_alpha):
    """
    Определяет, не столкнулся ли мяч со стеной, и если столкнулся,
    генерирует новое направление его движения (от стены)
    :param current_x: x-координата шарика
    :param current_y: x-координата шарика
    :param ball_r: радиус шарика
    :param changing_alpha: существующий угол между осью OX и вектором скорости
    :return: новый угол между осью OX и вектором скорости
    """
    if current_x < ball_r:    # Столкновение с левой стеной
        changing_alpha = randint(-4, 4) * math.pi / 10
    elif current_x > SCREEN_WIDTH - ball_r:    # Столкновение с правой стеной
        changing_alpha = randint(6, 14) * math.pi / 10
    elif current_y < ball_r:    # Столкновение с верхней стеной
        changing_alpha = randint(1, 9) * math.pi / 10
    elif current_y > SCREEN_HEIGHT - ball_r:    # Столкновение с нижней стеной
        changing_alpha = randint(11, 19) * math.pi / 10
    return changing_alpha


def click(pres_event):
    """
    Определяет, попал ли курсор в момент нажатия в какой-нибудь из шариков или квадратов 
    (если в несколько, то определяет, во сколько именно),
    Увеличивает количество очков и попыток и выводит результат попадания
    :param pres_event: событие, в частности, нажатие курсора
    """
    global SCORE, TRIES
    x_of_cursor, y_of_cursor = pres_event.pos
    TRIES += 1
    hits = 0
    for j in range(number_ob):
        x_of_ball = full_kin_data[j][0]
        y_of_ball = full_kin_data[j][1]
        r_of_ball = full_kin_data[j][2]
        distance = ((x_of_ball-x_of_cursor)**2 + (y_of_ball-y_of_cursor)**2) ** 0.5
        if r_of_ball >= distance:
            SCORE += 1
            hits += 1
            print('Ты попал в шарик №', j + 1)
    for j in range(number_tr):
        x_of_troll = full_kin_data_troll[j][0]
        y_of_troll = full_kin_data_troll[j][1]
        a_of_troll = full_kin_data_troll[j][2]
        x_dist = abs(x_of_troll - x_of_cursor)
        y_dist = abs(y_of_troll - y_of_cursor)
        if (a_of_troll / 2 >= x_dist) and (a_of_troll / 2 >= y_dist):
            SCORE += 2
            hits += 1
            print('Ого, ты попал в квадрат №', j + 1, 'это стоит целых 2 очка')
    if hits == 0:
        print('ахахахаха, мимо всех!')
    elif hits > 1:
        print('Вау,', hits, 'за раз!')
    print('ОЧКИ:', SCORE, ' ПОПЫТОК:', TRIES)


number_ob, full_kin_data = number_of_balls()
number_tr, full_kin_data_troll = number_of_trolls()

FPS = 30
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print('Click!')
            click(event)

    for i in range(number_ob):
        x, y, r, speed, alpha, color = full_kin_data[i]
        kin_data = mooving_ball(x, y, r,
                                speed, alpha, color)
        full_kin_data[i] = kin_data
    for i in range(number_tr):
        x, y, a, diff_a, speed, accel, alpha, color = full_kin_data_troll[i]
        kin_data_troll = mooving_troll_figure(x, y, a, diff_a,
                                              speed, accel, alpha, color)
        full_kin_data_troll[i] = kin_data_troll

    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()
