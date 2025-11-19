from .base import CommandGenerator

class RampCommand(CommandGenerator):
    def __init__(self, slope, offset=0):
        self.slope = slope
        self.offset = offset

    def get(self, t):
        return self.slope * t + self.offset

    def print(self, t):
        cmd_value = self.get(t)
        print("At time {:.2f}, command value is {:.2f}".format(t, cmd_value))
        return cmd_value

