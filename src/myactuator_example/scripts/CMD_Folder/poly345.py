import math
from .base import CommandGenerator

class Poly345Command(CommandGenerator):
    def __init__(self, amplitude1, amplitude2, period):
        self.A1 = amplitude1
        self.A2 = amplitude2
        self.T = period
    

    def get(self, t):
        abs_A1 = abs(self.A1)
        abs_A2 = abs(self.A2)
        t1 = abs_A1/(2*abs_A1 + 2*abs_A2)*self.T
        t2 = (abs_A1 + abs_A2)/(2*abs_A1 + 2*abs_A2)*self.T
        t3 = self.T-t2-t1
        if t < t1:
            cmd_value = self.A1*(10*(t/t1)**3-15*(t/t1)**4+6*(t/t1)**5)
            return cmd_value
        elif t < t1+t2:
            cmd_value = self.A1+(self.A2-self.A1)*(10*((t-t1)/t2)**3-15*((t-t1)/t2)**4+6*((t-t1)/t2)**5)
            return cmd_value
        elif t < t1+t2+t3:
            cmd_value = self.A2-self.A2*(10*((t-t1-t2)/t3)**3-15*((t-t1-t2)/t3)**4+6*((t-t1-t2)/t3)**5)
            return cmd_value
        else:
            cmd_value = 0 
            return cmd_value 
                   
    def print(self, t):
        cmd_value = self.get(t)
        print("At time {:.2f}, command value is {:.2f}".format(t, cmd_value))
        return cmd_value