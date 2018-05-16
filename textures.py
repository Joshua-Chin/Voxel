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
        return region.tex_coords

def block(side, top=None, bottom=None):
    if top is None:
        top = side
    if bottom is None:
        bottom = top
    return ('t3f', side * 4 + top + bottom)


textures = Textures('textures/')
group = textures.group

dirt = block(textures.dirt)
sand = block(textures.sand)
stone = block(textures.stone)
water = block(textures.water)
bedrock = block(textures.bedrock)
leaves = block(textures.leaves)
log = block(textures.log_oak, textures.log_oak_top)
grass = block(textures.grass_side, textures.grass_top, textures.dirt)
