import numpy as np
import math

class Transformation():
    def __init__(self, f, r=[0, 0, 0], t=[0, 0, 0]) -> None:
        self.r = r # r = (roll, pitch, yaw) in rand
        self.t = t # t = (dx, dy, dz)
        self.f = f
        self.T = np.eye(4)
        self.T = self.compute_transformation()

    def set_r(self, r):
        self.r = r
        self.T = self.compute_transformation()

    def set_t(self, t):
        self.t = t
        self.T = self.compute_transformation()        

    def inc_yaw(self, delta):
        self.set_r([self.r[0], self.r[1], self.r[2] + delta])
    
    def inc_pitch(self, delta):
        self.set_r([self.r[0], self.r[1] + delta, self.r[2]])
    
    def inc_roll(self, delta):
        self.set_r([self.r[0] + delta, self.r[1], self.r[2]])

    def inc_x(self, delta):
        self.set_t([self.t[0] + delta, self.t[1], self.t[2]])

    def inc_y(self, delta):
        self.set_t([self.t[0], self.t[1] + delta, self.t[2]])

    def inc_z(self, delta):
        self.set_t([self.t[0], self.t[1], self.t[2] + delta] )
    
        
    def compute_transformation(self):
        cr, cp, cy = np.cos(self.r)
        sr, sp, sy = np.sin(self.r)
        R = np.array(
            [
                [cy * cp, cy * sp * sr - sy * cr, cy * sp * cr + sy * sr],
                [sy * cp, sy * sp * sr + cy * cr, sy * sp * cr - cy * sr],
                [- sp, cp * sr, cp * cr],
            ]
        )
        self.T[:3, :3] = R
        self.T[:3, 3] = self.t
        return self.T