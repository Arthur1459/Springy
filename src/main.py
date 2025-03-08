import pygame as pg
from math import cos, sin, pi, tan
import tools as t
import utils as u
import vars as vr
import config as cf
import time

from node import SolidNode, Node
from spring import Spring, make_links

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
    #n1, n2, n3, n4 = Node((250, 250)), Node((650, 250)), Node((650, 650)), Node((250, 650))
    size = 30
    cf.gravity = 0
    sn1, sn2, sn3, sn4, sn5, sn6 = SolidNode((500, 150), size), SolidNode((500, 200), size), SolidNode((500, 250), size), SolidNode((500, 300), size), SolidNode((500, 350), size), SolidNode((500, 400), size)
    c1 = SolidNode((500, 100), size)
    vr.test_entities = [c1, sn1, sn2, sn3, sn4, sn5, sn6]
    vr.test_entities = vr.test_entities + make_links(((c1, sn1), (sn1, sn2), (sn2, sn3), (sn3, sn4), (sn4, sn5), (sn5, sn6)), k=0.1, extension=0.8)
    #vr.test_entities = vr.test_entities + make_links(((sn1, n1), (sn2, n2), (sn3, n3), (sn4, n4), (sn1, sn2), (sn2, sn3), (sn3, sn4), (sn4, sn1), (c1, sn1), (c1, sn2), (c1, sn3), (c1, sn4)))

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
        vr.test_entities[0].add_speed_by((1, 0, 10))
    elif vr.inputs['LEFT']:
        vr.test_entities[0].add_speed_by((-1, 0, -10))
    if vr.inputs['UP']:
        vr.test_entities[0].add_speed_by((0, -1, 0))
    elif vr.inputs['DOWN']:
        vr.test_entities[0].add_speed_by((0, 1, 0))

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