import os

from pyglet.gl import *
from pyglet.image.atlas import TextureAtlas
from pyglet.graphics import TextureGroup


class Textures(object):
    
    def __init__(self, path='./textures/'):
        self.atlas = TextureAtlas()
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        self.group = TextureGroup(self.atlas.texture)
        
        self.faces = faces = Faces()
        for image in os.listdir(path):
            setattr(self.faces, image[:-4], self.add(os.path.join(path, image)))

        self.dirt = self.block(faces.dirt)
        self.sand = self.block(faces.sand)
        self.stone = self.block(faces.stone)
        self.water = self.block(faces.water)
        self.bedrock = self.block(faces.bedrock)
        self.leaves = self.block(faces.leaves)
        self.log = self.block(faces.log_oak, faces.log_oak_top)
        self.grass = self.block(faces.grass_side, faces.grass_top, faces.dirt)

    def add(self, path):
        image = pyglet.image.load(path)
        region = self.atlas.add(image)
        return region.tex_coords

    def block(self, side, top=None, bottom=None):
        if top is None:
            top = side
        if bottom is None:
            bottom = top
        return ('t3f', side * 4 + top + bottom)

class Faces(object):
    pass
