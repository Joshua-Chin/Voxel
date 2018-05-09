import pyglet

class Window(pyglet.window.Window):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

def main():
    Window(resizable=True, caption="Joshua's Minecraft")
    pyglet.app.run()

if __name__ == '__main__':
    main()
