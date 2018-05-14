import os

from pyglet.gl import *
from pyglet.image.atlas import TextureAtlas
from pyglet.graphics import TextureGroup


class Textures(object):
    
    def __init__(self, path):
        self.atlas = TextureAtlas()
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        self.group = TextureGroup(self.atlas.texture)
        for image in os.listdir(path):
            setattr(self, image[:-4], self.add(os.path.join(path, image)))

    def add(self, path):
        image = pyglet.image.load(path)
        region = self.atlas.add(image)
        return ('t3f', region.tex_coords)
