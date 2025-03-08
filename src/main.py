import pygame as pg
from math import cos, sin, pi, tan
import tools as t
import utils as u
import vars as vr
import config as cf
import time

from node import SolidNode
from spring import Spring

def init():

    pg.init()
    pg.display.set_caption(cf.game_name)

    # screen initialisation
    if not cf.fullscreen:
        vr.window = pg.display.set_mode(vr.window_size)
    else:
        vr.window = pg.display.set_mode((0, 0), pg.FULLSCREEN)
        vr.window_size = vr.window.get_size()

    vr.clock = pg.time.Clock()

    u.InitEntityGrid()

    return

def main():
    init()

    # Test
    vr.test_entities.append(SolidNode((550, 400, 0), 25))
    vr.test_entities.append(SolidNode((300, 300, 0), 25))
    vr.test_entities.append(Spring(vr.test_entities[0], vr.test_entities[1]))
    # End Test

    vr.running = True

    frames_fps, t_fps = 0, time.time() - 1

    while vr.running:

        vr.clock.tick(cf.fps)

        vr.t = time.time()
        frames_fps += 1
        vr.fps = frames_fps/(vr.t - t_fps)
        vr.dt = 1
        if frames_fps > 1000:
            frames_fps, t_fps = 0, time.time()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                vr.running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                print("Cursor : ", pg.mouse.get_pos())

        # Main Loop #
        pre_update()
        if vr.fps > cf.fps * cf.fps_treshold:
            update()
        post_update()
        # --------- #

    return

def update():
    vr.cursor = pg.mouse.get_pos()

    if vr.inputs['RIGHT']:
        vr.test_entities[0].add_speed_by((5, 0, 10))
    elif vr.inputs['LEFT']:
        vr.test_entities[0].add_speed_by((-5, 0, -10))
    if vr.inputs['UP']:
        vr.test_entities[0].add_speed_by((0, -5, 0))
    elif vr.inputs['DOWN']:
        vr.test_entities[0].add_speed_by((0, 5, 0))

    for entity in vr.test_entities:
        entity.update()
        entity.draw()
    return

def pre_update():
    u.getInputs()
    vr.window.fill('black')

def post_update():
    u.Text("fps : " + str(round(vr.fps, 1)), (10, vr.win_height - 24), 14, 'orange')
    u.Text("info : " + str(vr.info_txt), (10, vr.win_height - 48), 14, 'orange')
    pg.display.update()
    return

if __name__ == "__main__":
    main()