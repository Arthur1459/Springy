import utils as u
import tools as t
import vars as vr
import config as cf

import pygame as pg

class Node:
    def __init__(self, coordi, size=0, speedi=(0, 0, 0), acceli=(0, 0, 0), color=cf.colors['node']):
        self.id = u.getNewId()
        self.type_name = 'node'
        self.tags = {'node'}
        self.oneshot_tags = {}

        self.size = size
        self.color = color

        self.coord = list(coordi) if len(coordi) == 3 else list(coordi) + [0]
        self.coord_at_last_update = list(coordi) if len(coordi) == 3 else list(coordi) + [0]
        self.speed_pushed = list(speedi) if len(speedi) == 3 else list(speedi) + [0]
        self.accel = list(acceli) if len(acceli) == 3 else list(acceli) + [0]

        self.pos = u.coord_to_pos(self.coord)
        self.pos_at_last_update = self.pos

        vr.entity_grid[self.pos][self.id] = self

    def move_to(self, coord):
        if len(coord) == 2: self.coord = list(coord) + [0]
        else: self.coord = coord
    def set_to(self, coord):
        if len(coord) == 2: self.coord = list(coord) + [0]
        else: self.coord = coord
        self.coord_at_last_update = self.coord[:]
    def add_speed_by(self, speed_added):
        self.speed_pushed = t.Vadd(self.speed_pushed, speed_added)
    def add_accel_by(self, accel_added):
        self.accel = t.Vadd(self.accel, accel_added)
    def get_angle(self):
        return u.angle(self.coord)
    def get_xy(self):
        return u.x(self.coord), u.y(self.coord)

    def update_pos(self):
        self.pos = u.coord_to_pos(self.coord)
        if self.pos != self.coord_at_last_update:
            del vr.entity_grid[self.pos_at_last_update][self.id]
            self.pos_at_last_update = self.pos
            vr.entity_grid[self.pos][self.id] = self

    def update(self):
        self.coord = self.coord_at_last_update
        self.update_pos()
        self.oneshot_tags = {}
    def draw(self):
        pg.draw.line(vr.window, (120, 120, 120), (u.x(self.coord) - 15, u.y(self.coord)), (u.x(self.coord) + 15, u.y(self.coord)), width=3)
        pg.draw.line(vr.window, (120, 120, 120), (u.x(self.coord), u.y(self.coord) + 15), (u.x(self.coord), u.y(self.coord) - 15), width=3)

class MovingNode(Node):
    def __init__(self, coordi, size=1, speedi=(0, 0, 0), acceli=(0, 0, 0), color=cf.colors['movingnode']):
        super().__init__(coordi, size, speedi, acceli, color)
        self.type_name = 'movingnode'

    def update(self):
        self.coord_at_last_update = self.coord
        # Apply physics
        self.accel = (0, 0, 0)
        self.speed_pushed = t.Vadd(self.speed_pushed, t.Vmul(self.accel, vr.dt))
        self.coord = u.keepInWindow(
            t.Vsum(self.coord, t.Vmul(self.speed_pushed, vr.dt)),
            dx=self.size, dy=self.size)

        self.accel = (0, 0, 0)
        self.speed_pushed = t.Vmul(self.speed_pushed, 0.95)

        # update ppos
        self.update_pos()
        self.oneshot_tags = {}

    def draw(self):
        pg.draw.line(vr.window, (160, 160, 0), (u.x(self.coord) - 15, u.y(self.coord)), (u.x(self.coord) + 15, u.y(self.coord)), width=3)
        pg.draw.line(vr.window, (160, 160, 0), (u.x(self.coord), u.y(self.coord) + 15), (u.x(self.coord), u.y(self.coord) - 15), width=3)

class SolidNode(Node):
    def __init__(self, coordi, sizei, speedi=(0, 0, 0), acceli=(0, 0, 0), color=cf.colors['solidnode']):
        super().__init__(coordi, sizei, speedi, acceli, color)
        self.type_name = 'solidnode'
        self.tags = {'node', 'solidnode', 'collide'}

    def update(self):

        # Update pos in grid because might have been pushed since last update
        self.update_pos()

        # Collide
        line, col = self.pos
        neighboors = {'TOPLEFT': (line - 1, col - 1), 'TOP': (line - 1, col), 'TOPRIGHT': (line - 1, col + 1),
                      'LEFT': (line, col + 1), 'CENTER': (line, col), 'RIGHT': (line, col + 1),
                      'BOTLEFT': (line, col - 1), 'BOT': (line + 1, col), 'BOTRIGHT': (line + 1, col + 1)}
        for grid_pos in neighboors:
            if not u.isInGrid(neighboors[grid_pos]): continue
            for entity_id in vr.entity_grid[neighboors[grid_pos]]:
                entity = vr.entity_grid[neighboors[grid_pos]][entity_id]
                if entity.id != self.id and 'collide' in entity.tags:
                    if 'node' in entity.tags:
                        dist_min = self.size + entity.size
                        overlap = dist_min - t.distance(entity.get_xy(), self.get_xy())
                        if overlap > 0 :
                            direction = t.Vdir(self.get_xy(), entity.get_xy())
                            self.move_to(t.Vcl(1, self.get_xy(), -1 * overlap * (entity.size / dist_min) * 0.5, direction))
                            entity.move_to(t.Vcl(1, entity.get_xy(), 1 * overlap * (self.size / dist_min) * 0.5, direction))

        # Apply physics
        if 'nophysics' not in self.oneshot_tags:
            accel_applied = t.Vadd((0, cf.gravity if 'nogravity' not in self.oneshot_tags else 0, 0), self.accel)
            self.speed_pushed = t.Vadd(self.speed_pushed, t.Vmul(self.accel, vr.dt))
            speed_applied = t.Vsum(t.Vmul(t.Vdiff(self.coord, self.coord_at_last_update), t.inv(vr.dt)), self.speed_pushed)
            self.coord = u.keepInWindow(t.Vsum(self.coord_at_last_update, t.Vmul(speed_applied, vr.dt),  t.Vmul(accel_applied, 0.5 * (vr.dt ** 2))), dx=self.size, dy=self.size)

            self.accel = (0, 0, 0)
            self.speed_pushed = t.Vmul(self.speed_pushed, 0.95)
        else:
            self.accel = (0, 0, 0)
            self.speed_pushed = t.Vmul(t.Vdiff(self.coord, self.coord_at_last_update), t.inv(vr.dt))
            self.coord_at_last_update = self.coord

        # Update pos in grid after having moved
        self.update_pos()
        self.oneshot_tags = {}

    def draw(self):
        pg.draw.circle(vr.window, self.color, self.get_xy(), self.size)
        #pg.draw.line(vr.window, (190, 125, 0), self.get_xy(), t.makeVect(self.get_xy(), t.radians(self.get_angle()), self.size), width=int(self.size / 10))

class NodeShape:
    def __init__(self, nodes):
        self.id = u.getNewId()
        self.tags = {'nodeshape'}
        self.nodes = nodes

    def update(self):
        pass

    def draw(self):
        pg.draw.polygon(vr.window, (150, 150, 0), [n.get_xy() for n in self.nodes])
