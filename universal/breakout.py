"""
CircuitPython code by Thierry Chantier
"""
import pew
from random import randint


def inputs(pad):
    keys = pew.keys()
    if keys & pew.K_LEFT and pad['X'] > 0:
        pad['X'] -= 1
    elif keys & pew.K_RIGHT and pad['X'] < 8 - pad['WIDTH']:
        pad['X'] += 1


def updates(pad, ball):
    # update ball
    ball['X'] += ball['VX']
    ball['Y'] += ball['VY']

    # Collision with walls
    if ball['X'] <= 0 or ball['X'] > 8 - ball['SIZE']:
        ball['VX'] *= -1

    if ball['Y'] < 0:
        ball['VY'] *= -1
    elif ball['Y'] >= 7:
        reinit(pad, ball)

    # ball and pad collision
    if ball['Y'] == 6 and (pad['X'] <= ball['X'] <= pad['X'] + pad['WIDTH']):
        ball['VY'] = -1  # up


def reinit(pad, ball):
    ball['X'] = randint(0, 8 - ball['SIZE'])
    ball['Y'] = pad['Y'] - ball['SIZE']  # Just above the pad
    ball['VX'] = 1  # left
    ball['VY'] = -1  # up


def draw(screen, pad, ball):
    screen.box(0, 0, 0, 8, 8)
    screen.box(pad['COLOR'], pad['X'], pad['Y'], pad['WIDTH'], pad['HEIGHT'])
    screen.box(ball['COLOR'], ball['X'], ball['Y'], ball['WIDTH'], ball['HEIGHT'])


pew.init()
g_screen = pew.Pix()

# Pad characteristics
g_pad = {
    'X': 2,
    'Y': 7,
    'WIDTH': 2,
    'HEIGHT': 1,
    'COLOR': 3
}

# ball characteristics
g_ball = {
    'X': 4,
    'Y': 2,
    'VX': 1,
    'VY': 1,
    'WIDTH': 1,
    'HEIGHT': 1,
    'SIZE': 1,
    'COLOR': 1
}

while True:
    inputs(g_pad)

    updates(g_pad, g_ball)

    draw(g_screen, g_pad, g_ball)

    pew.show(g_screen)
    pew.tick(1 / 4)
