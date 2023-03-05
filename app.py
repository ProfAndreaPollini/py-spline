import scipy.interpolate as si
import numpy as np
import pygame as pg


pg.init()

SIZE = 800, 600

screen = pg.display.set_mode(SIZE)
clock = pg.time.Clock()
running = True


# https://stackoverflow.com/a/34807513

def bspline(cv, n=100, degree=3, periodic=False):
    """ Calculate n samples on a bspline

        cv :      Array ov control vertices
        n  :      Number of samples to return
        degree:   Curve degree
        periodic: True - Curve is closed
                  False - Curve is open
    """

    # If periodic, extend the point array by count+degree+1
    cv = np.asarray(cv)
    count = len(cv)

    if periodic:
        factor, fraction = divmod(count+degree+1, count)
        cv = np.concatenate((cv,) * factor + (cv[:fraction],))
        count = len(cv)
        degree = np.clip(degree, 1, degree)

    # If opened, prevent degree from exceeding count-1
    else:
        degree = np.clip(degree, 1, count-1)

    # Calculate knot vector
    kv = None
    if periodic:
        kv = np.arange(0-degree, count+degree+degree-1, dtype='int')
    else:
        kv = np.concatenate(
            ([0]*degree, np.arange(count-degree+1), [count-degree]*degree))

    # Calculate query range
    u = np.linspace(periodic, (count-degree), n)

    # Calculate result
    return np.array(si.splev(u, (kv, cv.T, degree))).T


points = []
evaluted_points = []


def update_splines():
    global evaluted_points
    evaluted_points = bspline(points)


while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pg.mouse.get_pos()
            points.append((mouse_x, mouse_y))
            update_splines()

        screen.fill((55, 55, 55))

        for i in range(len(evaluted_points)-1):
            pg.draw.aaline(screen, (255, 0, 0),
                           evaluted_points[i], evaluted_points[i+1])

        pg.display.update()

pg.quit()
