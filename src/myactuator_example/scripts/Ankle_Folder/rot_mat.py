import numpy as np
from math import sin,cos
def rot_x(th):
    c = cos(th)
    s = sin(th)
    mat = np.array([[1,0,0],
                    [0,c,-s],
                    [0,s,c]])
    return (mat)

def rot_y(th):
    c = cos(th)
    s = sin(th)
    mat = np.array([[c,0,s],
                    [0,1,0],
                    [-s,0,c]])
    return (mat)
