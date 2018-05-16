import math

import pyglet.image as image
import pyglet.graphics as graphics

from pyglet.gl import *
from pyglet.window import key

import textures

class Model(object):

    def __init__(self):
        self.group = textures.group
        self.batch = pyglet.graphics.Batch()
        self.blocks = {}

        for i in range(-10, 10):
            for j in range(-10, 10):
                self.add_block((i,0,j), textures.grass)

        for i in range(-2, 3):
            self.add_block((0, i +3, 0), textures.log)
            for j in range(-2, 3):
                for k in range(-2, 3):
                    self.add_block((i, j+5, k), textures.leaves)


    def add_block(self, position, tex_coords):
        (x, X), (y, Y), (z, Z) = [(coord-0.5, coord+0.5) for coord in position]
        vertices = ('v3f', [
            X,y,z, x,y,z, x,Y,z, X,Y,z, # front
            x,y,Z, X,y,Z, X,Y,Z, x,Y,Z, # back
            x,y,z, x,y,Z, x,Y,Z, x,Y,z, # left
            X,y,Z, X,y,z, X,Y,z, X,Y,Z, # right
            x,Y,Z, X,Y,Z, X,Y,z, x,Y,z, # top
            x,y,z, X,y,z, X,y,Z, x,y,Z, # bottom
        ])
        
        ns, ew, top, bottom = (0.8,) * 12, (0.6,) * 12, (1.0,) * 12, (0.5,) * 12
        color_coords = ('c3f', ns * 2 + ew * 2 + top + bottom)

        data = vertices, tex_coords, color_coords
        vertexlist = self.batch.add(24, GL_QUADS, self.group, *data)
        self.blocks[position] = vertexlist

    def draw(self):
        self.batch.draw()

class Player(object):
     
    def __init__(self):
         self.pos = [0, 3, 0]
         self.rot = [0, 0]

    def update(self, dt, keys):
        s = 10 * dt
        rotY = (math.pi / 180) * self.rot[1]
        dx, dz = s * math.sin(rotY), s * math.cos(rotY)
        if keys[key.W]:
            self.pos[0] += dx
            self.pos[2] -= dz
        if keys[key.S]:
            self.pos[0] -= dx
            self.pos[2] += dz
        if keys[key.A]:
            self.pos[0] -= dz
            self.pos[2] -= dx
        if keys[key.D]:
            self.pos[0] += dz
            self.pos[2] += dx

        if keys[key.SPACE]:
            self.pos[1] += s
        if keys[key.LSHIFT]:
            self.pos[1] -= s

    def on_mouse_motion(self, x, y, dx, dy):
        self.rot[0] += dy / 4
        self.rot[1] += dx / 4
        self.rot[0] = max(-90, min(90, self.rot[0]))

class Window(pyglet.window.Window):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        glEnable(GL_ALPHA_TEST)
        glAlphaFunc(GL_GREATER, 0.0)
        glClearColor(.52, .80, .91, 1.0)

        self.set_minimum_size(400, 300)
        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)
        pyglet.clock.schedule(self.update)
        
        self.model = Model()
        self.player = Player()
        self._lock = False

    def update(self, dt):
        self.player.update(dt, self.keys)

    def projection(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity() 
    
    def modelview(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def set3d(self):
        self.projection()
        gluPerspective(70, self.width/self.height, 0.5, 1000)
        self.modelview()

    def set2d(self):
        self.projection()
        gluOrtho2D(0, self.width, 0, self.height)
        self.modelview()

    def on_draw(self):
        self.clear()
        self.set3d()
        rot = self.player.rot
        glRotatef(-rot[0], 1, 0, 0)
        glRotatef(rot[1], 0, 1, 0)
        x, y, z = self.player.pos
        glTranslatef(-x, -y, -z)
        self.model.draw()
    
    def on_key_press(self, k, modifier):
        if k == key.ESCAPE:
            self.close()

    def on_mouse_motion(self, x, y, dx, dy):
        self.player.on_mouse_motion(x, y, dx, dy)
    

def main():
    window = Window(resizable=True, caption="Joshua's Minecraft")
    window.set_exclusive_mouse(True)
    pyglet.app.run()

if __name__ == '__main__':
    main()
