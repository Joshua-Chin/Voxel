import random
import math
from collections import defaultdict

class Perlin(object):

    def __init__(self, period, magnitude=None):
        if magnitude is None:
            magnitude = period
        self.period = period
        self.magnitude = magnitude
        self.gradients = defaultdict(random_unit_vector)

    def __getitem__(self, pos):
        x, y = pos
        p = self.period
        g = self.gradients
        x0, y0 = p * (x // p), p * (y // p)
        x1, y1 = x0 + p, y0 + p
        
        n00 = dot(g[x0, y0], ((x0-x)/p, (y0-y)/p))
        n10 = dot(g[x1, y0], ((x1-x)/p, (y0-y)/p))
        n01 = dot(g[x0, y1], ((x0-x)/p, (y1-y)/p))
        n11 = dot(g[x1, y1], ((x1-x)/p, (y1-y)/p))
        
        n0 = interpolate((x-x0)/p, n00, n10)
        n1 = interpolate((x-x0)/p, n01, n11)

        n = interpolate((y-y0)/p, n0, n1)
        return n * self.magnitude


class Octave(object):
    
    def __init__(self, octaves, magnitude=None):
        if magnitude is None:
            magnitude = 1
        self.octaves = [Perlin(2 ** n) for n in range(octaves)]
        self.magnitude = magnitude / 2 ** octaves

    def __getitem__(self, pos):
        total = 0
        for log_period, noise in enumerate(self.octaves):
            total += noise[pos]
        return total * self.magnitude


class Combined(object):

    def __init__(self, noise1, noise2):
        self.noise1 = noise1
        self.noise2 = noise2

    def __getitem__(self, pos):
        x, y = pos
        return self.noise1[x + self.noise2[x, y], y]


def dot(v1, v2):
    return v1[0] * v2[0] + v1[1] * v2[1]

def interpolate(x, a0, a1):
    return a0 + smoothstep(x) * (a1 - a0)

def smoothstep(x):
    return ((6 * x - 15) * x + 10) * x * x * x

def random_unit_vector():
    angle = random.uniform(0, 2 * math.pi)
    return math.sin(angle), math.cos(angle)
