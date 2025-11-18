import math
from .base import CommandGenerator

class Poly345Command(CommandGenerator):
    def __init__(self, amplitude1, amplitude2, period, offset=0):
        self.A1 = amplitude1
        self.A2 = amplitude2
        self.T = period
        self.offset = offset

    def get(self, t):
        if t < self.T/3:
            return self.A1*(10*(t/self.T)^3-15*(t/self.T)^4+6*(t/self.T)^5)
        elif t < self.T*2/3:
            return self.A1*(10*(t/self.T)^3-15*(t/self.T)^4+6*(t/self.T)^5)
        elif t < self.T:
            return self.A1*(10*(t/self.T)^3-15*(t/self.T)^4+6*(t/self.T)^5)
           

