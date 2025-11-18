from .base import CommandGenerator

class RampCommand(CommandGenerator):
    def __init__(self, slope, offset=0):
        self.slope = slope
        self.offset = offset

    def get(self, t):
        return self.slope * t + self.offset

