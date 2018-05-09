import math

from pyglet.gl import *
from pyglet.window import key

class Model(object):

    def __init__(self):
        self.top = self.get_texture('grass_top.png')
        self.side = self.get_texture('grass_side.png')
        self.bottom = self.get_texture('dirt.png')

        self.batch = pyglet.graphics.Batch()

        x,y,z = 0,0,-1
        X,Y,Z = x+1,y+1,z+1

        tex_coords = ('t2f', (0,0, 1,0, 1,1, 0,1))

        self.batch.add(4, GL_QUADS, self.side,
            ('v3f', [x,y,z, X,y,z, X,Y,z, x,Y,z]), tex_coords)

    def draw(self):
        self.batch.draw()

    def get_texture(self, file):
        texture = pyglet.image.load(file).texture
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        return pyglet.graphics.TextureGroup(texture)

class Player(object):
     
    def __init__(self):
         self.pos = [0, 0, 0]
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

class Window(pyglet.window.Window):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_minimum_size(400, 300)
        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)
        pyglet.clock.schedule(self.update)

        glClearColor(.52, .80, .91, 1)
        
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
        # glRotatef(-30, 1, 0, 0)
        x, y, z = self.player.pos
        glTranslatef(-x, -y, -z)
        self.model.draw()
    
    def on_key_press(self, k, modifier):
        if k == key.ESCAPE:
            self.close()
        elif k == key.SPACE:
            self.mouse_lock = not self.mouse_lock

    @property
    def mouse_lock(self):
        return self._lock

    @mouse_lock.setter
    def mouse_lock(self, state):
        self._lock = state
        self.set_exclusive_mouse(state)
    

def main():
    Window(resizable=True, caption="Joshua's Minecraft")
    pyglet.app.run()

if __name__ == '__main__':
    main()
