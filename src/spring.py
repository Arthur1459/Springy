import utils as u
import tools as t
import vars as vr
import config as cf
from node import SolidNode

import pygame as pg

class Spring:
    def __init__(self, node_1: SolidNode, node_2: SolidNode, k=0.02, extension_i=1): # k < 0.2 better
        self.id = u.getNewId()
        self.type_name = 'solidnode'
        self.tags = {'spring'}
        self.node_1, self.node_2 = node_1, node_2
        self.k_0, self.k_applied = k, k
        self.len_0 = t.distance(self.node_1.get_xy(), self.node_2.get_xy()) / extension_i

    def get_extension(self):
        return t.distance(self.node_1.get_xy(), self.node_2.get_xy()) - self.len_0

    def update(self):
        self.k_applied = self.k_0 * (1 + abs(2 * self.get_extension()/self.len_0))
        force = t.Vmul(t.Vdir(self.node_1.coord, self.node_2.coord), self.k_applied * self.get_extension())
        force[2] = 0
        if t.norm(force) > 50:
            force = t.Vmul(t.normalise(force), 50)
        self.node_1.add_accel_by(t.Vmul(force, 1))
        self.node_2.add_accel_by(t.Vmul(force, -1))

    def draw(self):
        nb_pts, offset, teeth_size = 40, 6, 15
        center_seg = t.makeSeg(self.node_1.get_xy(), self.node_2.get_xy())
        points = [center_seg(d/nb_pts) for d in range(offset, nb_pts - offset + 1)]

        v_segment = t.Vdiff(points[1], points[0])
        side_dir = t.normalise([-v_segment[1], v_segment[0]])

        point_for_lines = [center_seg(0), center_seg(offset/nb_pts)] + [t.Vadd(center_seg(0), t.Vadd(t.Vmul(v_segment, i), t.Vmul(side_dir, teeth_size * (1 if (i % 4 == 2) else (-1 if (i % 4 == 0) else 0))))) for i in range(offset, nb_pts - offset + 1)] + [center_seg(1 - offset/nb_pts), center_seg(1)]

        c_factor = min(max(50 * self.k_applied * abs(self.get_extension()) / self.len_0, 0), 1)
        pg.draw.lines(vr.window, (255 * c_factor, 190 * (1 - c_factor), 0), False, point_for_lines, 3)

def make_links(pair_to_link, k=0.05, extension=1):
    springs = []
    for n1, n2 in pair_to_link:
        springs.append(Spring(n1, n2, k, extension))
    return springs
