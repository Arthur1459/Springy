import utils as u
import tools as t
import vars as vr
import config as cf
from node import SolidNode

import pygame as pg

class Spring:
    def __init__(self, node_1: SolidNode, node_2: SolidNode):
        self.id = u.getNewId()
        self.tags = {'spring'}
        self.node_1, self.node_2 = node_1, node_2
        self.k_0 = 0.02
        self.len_0 = t.distance(self.node_1.get_xy(), self.node_2.get_xy())
    def get_extension(self):
        return t.distance(self.node_1.get_xy(), self.node_2.get_xy()) - self.len_0

    def update(self):
        k_applied = self.k_0 * (1 + abs(2 * self.get_extension()/self.len_0))
        force = t.Vmul(t.Vdir(self.node_1.coord, self.node_2.coord), k_applied * self.get_extension())
        force[2] = 0
        self.node_1.add_accel_by(t.Vmul(force, 1))
        self.node_2.add_accel_by(t.Vmul(force, -1))

    def draw(self):
        pg.draw.line(vr.window, (max(min(255 * 2 * self.get_extension() / self.len_0, 255), 50), 0, 0), self.node_1.get_xy(), self.node_2.get_xy(), 3)

