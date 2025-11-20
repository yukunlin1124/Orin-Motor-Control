import numpy as np
from math import sin,cos,atan,asin,sqrt

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


class Ankle:
    def __init__(self):
        self.__P0_a1 = np.array([0,-50.25,165])
        self.__P0_a2 = np.array([0,50.25,241.5])
        self.__P0_c1 = np.array([-42.5,-30.75,0])
        self.__P0_c2 = np.array([-42.5,30.75,0])
        self.__l_bar1 = -55
        self.__l_bar2 = -55
        self.__l_rod1 = 155.5
        self.__l_rod2 = 230.5
    
    def IK(self,th_p,th_r): # in rad
        P_c1 = (rot_y(th_p)@rot_x(th_r)@(self.__P0_c1[:, np.newaxis])).flatten()
        P_c2 = (rot_y(th_p)@rot_x(th_r)@(self.__P0_c2[:, np.newaxis])).flatten()
        A1 = 2*self.__l_bar1*(P_c1[0]-self.__P0_a1[0])
        B1 = 2*self.__l_bar1*(P_c1[2]-self.__P0_a1[2])
        C1 = P_c1[0]**2+self.__P0_a1[0]**2+P_c1[1]**2+self.__P0_a1[1]**2+P_c1[2]**2+self.__P0_a1[2]**2+self.__l_bar1**2-self.__l_rod1**2-2*(P_c1[0]*self.__P0_a1[0]+P_c1[1]*self.__P0_a1[1]+P_c1[2]*self.__P0_a1[2])
    
        A2 = 2*self.__l_bar2*(P_c2[0]-self.__P0_a2[0])
        B2 = 2*self.__l_bar2*(P_c2[2]-self.__P0_a2[2])
        C2 = P_c2[0]**2+self.__P0_a2[0]**2+P_c2[1]**2+self.__P0_a2[1]**2+P_c2[2]**2+self.__P0_a2[2]**2+self.__l_bar2**2-self.__l_rod2**2-2*(P_c2[0]*self.__P0_a2[0]+P_c2[1]*self.__P0_a2[1]+P_c2[2]*self.__P0_a2[2])

        th1 = atan(A1/B1)-asin(C1/sqrt(A1**2+B1**2))
        th2 = atan(A2/B2)-asin(C2/sqrt(A2**2+B2**2))
        return th1,th2
    def FK(self):
        pass