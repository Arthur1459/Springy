import os
import sys

import pygame as pg
from time import time

import vars as vr
import config as cf


def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def Text(msg, coord, size, color):  # blit to the screen a text
    TextColor = pg.Color(color) # set the color of the text
    font = pg.font.Font(resource_path("rsc/pixel.ttf"), size)  # set the font
    return vr.window.blit(font.render(msg, True, TextColor), coord)  # return and blit the text on the screen

def getInputs():
    keys = pg.key.get_pressed()
    vr.inputs["SPACE"] = True if keys[pg.K_SPACE] else False

    vr.inputs["UP"] = True if keys[pg.K_UP] else False
    vr.inputs["DOWN"] = True if keys[pg.K_DOWN] else False
    vr.inputs["RIGHT"] = True if keys[pg.K_RIGHT] else False
    vr.inputs["LEFT"] = True if keys[pg.K_LEFT] else False

def x(vect):
    return vect[0]
def y(vect):
    return vect[1]
def angle(vect):
    return vect[2]

def isInWindow(coord):
    if 0 <= x(coord) <= vr.win_width:
        if 0 <= y(coord) <= vr.win_height:
            return True
    return False

def isInGrid(pos):
    line, col = pos
    if 0 <= line < cf.entity_grid_factor:
        if 0 <= col < cf.entity_grid_factor:
            return True
    return False

def keepInWindow(coord, dx=0, dy=0):
    return [min(max(0, x(coord) - dx) + 2 * dx, vr.win_width) - dx, min(max(0, y(coord) - dy) + 2 * dy, vr.win_height) - dy, angle(coord)]

def makeSeg(a, b):
    return lambda t: (b[0] + (t - 1) * (b[0] - a[0]), b[1] + (t - 1) * (b[1] - a[1]))

def cross_product(v1, v2):
    return v1[0] * v2[1] - v1[1] * v2[0]

def drawSeg(seg):
    pg.draw.line(vr.window, (20, 20, 100), seg(0), seg(1), 4)

def getNewId():
    vr.id += 1
    return vr.id

def InitEntityGrid():
    for line in range(cf.entity_grid_factor):
        for col in range(cf.entity_grid_factor):
            vr.entity_grid[(line, col)] = {}

def coord_to_pos(coord):
    return min(max(int(cf.entity_grid_factor * y(coord) / vr.win_height), 0), cf.entity_grid_factor - 1), min(max(int(cf.entity_grid_factor * x(coord) / vr.win_width), 0), cf.entity_grid_factor - 1)

def pos_to_coord(pos, offset=0.):
    return vr.win_width * (pos[1] + offset) / cf.entity_grid_factor, vr.win_height * (pos[0] + offset) / cf.entity_grid_factor

def wait_key(dt=0.2, reset=True):
    t = time()
    if t - vr.wait_key > dt:
        if reset: vr.wait_key = t
        return True
    else: return False
