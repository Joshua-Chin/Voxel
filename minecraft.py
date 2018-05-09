from pyglet.gl import *


class Model(object):

    def __init__(self):
        self.batch = pyglet.graphics.Batch()

        x,y,z = 0,0,-1
        X,Y,Z = x+1,y+1,z+1

        color = ('c3f', (1,1,1) * 4)

        self.batch.add(4, GL_QUADS, None,
            ('v3f', [x,y,z, X,y,z, X,Y,z, x,Y,z]), color)

    def draw(self):
        self.batch.draw()

class Window(pyglet.window.Window):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_minimum_size(400, 300)
        glClearColor(.52, .80, .91, 1)
        self.model = Model()

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
        self.model.draw()

def main():
    Window(resizable=True, caption="Joshua's Minecraft")
    pyglet.app.run()

if __name__ == '__main__':
    main()
