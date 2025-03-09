import pygame as pg
from math import cos, sin, pi, tan
import tools as t
import utils as u
import vars as vr
import config as cf
import time

from node import SolidNode, Node, MovingNode, NodeShape
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
    vr.inputs['CLICK'] = False

    # Test
    n1, n2, n3, n4 = Node((250, 250)), Node((650, 250)), Node((650, 650)), Node((250, 650))
    mn1 = SolidNode((450, 450), 25)
    size = 25
    sn0, sn1, sn2, sn3, sn4, sn5, sn6, sn7 = SolidNode((300, 300), size), SolidNode((450, 250), size), SolidNode((600, 300), size), SolidNode((650, 450), size), SolidNode((600, 600), size), SolidNode((450, 650), size), SolidNode((300, 600), size), SolidNode((250, 450), size)
    vr.test_entities = [mn1, sn0, sn1, sn2, sn3, sn4, sn5, sn6, sn7]
    #vr.test_entities = vr.test_entities + make_links(((n1, sn2), (sn2, sn3), (sn3, sn4), (sn4, sn5), (sn5, n4)), k=0.2, extension=1)
    #vr.test_entities = vr.test_entities + make_links(((sn1, n1), (sn2, n2), (sn3, n3), (sn4, n4)), k=0.05)
    vr.test_entities = vr.test_entities + make_links(((sn0, sn1), (sn1, sn2), (sn2, sn3), (sn3, sn4), (sn4, sn5), (sn5, sn6), (sn6, sn7), (sn7, sn0)), k=0.02)
    vr.test_entities = vr.test_entities + make_links(((sn0, sn2), (sn1, sn3), (sn2, sn4), (sn3, sn5), (sn4, sn6), (sn5, sn7), (sn6, sn0), (sn7, sn1)), k=0.02)
    vr.test_entities = vr.test_entities + make_links(((mn1, sn0), (mn1, sn1), (mn1, sn2), (mn1, sn3), (mn1, sn4), (mn1, sn5), (mn1, sn6), (mn1, sn7)), k=0.1)

    vr.test_entities.append(NodeShape([sn0, sn1, sn2, sn3, sn4, sn5, sn6, sn7]))
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
                vr.inputs['CLICK'] = True
            elif event.type == pg.MOUSEBUTTONUP:
                vr.inputs['CLICK'] = False

        # Main Loop #
        pre_update()
        if vr.fps > cf.fps * cf.fps_treshold:
            update()
        post_update()
        # --------- #

    return

def update():
    vr.cursor = pg.mouse.get_pos()

    if vr.inputs['SPACE'] and u.wait_key(): vr.toggle_shape = False if vr.toggle_shape else True
    vr.info_txt = "shape mode : " + ('on' if vr.toggle_shape else 'off')

    for entity in vr.test_entities:
        if 'solidnode' in entity.tags:
            if t.distance(entity.get_xy(), vr.cursor) < entity.size:
                if vr.inputs['CLICK']:
                    entity.color = (200, 110, 230)
                    entity.oneshot_tags = {'nophysics'}
                    entity.set_to(vr.cursor)
                else:
                    entity.color = (150, 50, 180)
                    entity.update()
            else:
                entity.color = cf.colors[entity.type_name]
                entity.update()
        else:
            entity.update()
        if vr.toggle_shape:
            if 'nodeshape' in entity.tags:
                entity.draw()
        elif 'nodeshape' not in entity.tags:
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