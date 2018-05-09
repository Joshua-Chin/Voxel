from pyglet.gl import *


class Window(pyglet.window.Window):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_minimum_size(400, 300)

        glClearColor(.52, .80, .91, 1)

    def on_draw(self):
        self.clear()


def main():
    Window(resizable=True, caption="Joshua's Minecraft")
    pyglet.app.run()


if __name__ == '__main__':
    main()
