import math
from .base import CommandGenerator

class SineCommand(CommandGenerator):
    def __init__(self, amplitude, frequency, offset=0):
        self.A = amplitude
        self.f = frequency
        self.offset = offset

    def get(self, t):
        return self.A * math.sin(2*math.pi*self.f*t) + self.offset

