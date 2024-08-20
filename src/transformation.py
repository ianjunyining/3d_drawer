import numpy as np
import math
import src.geometry as geo

class Transformation():
    def __init__(self, f, r=[0, 0, 0], t=[0, 0, 0]) -> None:
        self.r = r # r = (roll, pitch, yaw) in rand
        self.t = t # t = (dx, dy, dz)
        self.f = f
        self.T = np.eye(4)
        self.T = self.compute_transformation()

    def reset(self):
        self.f=1000
        self.r=(math.pi / 4, math.pi / 4, math.pi / 4)
        self.t=(0, 0, 5000)
        self.T = self.compute_transformation()

    def set_r(self, r):
        self.r = r
        self.T = self.compute_transformation()

    def set_t(self, t):
        self.t = t
        self.T = self.compute_transformation()        

    def rotate(self, delta):
        self.set_r(geo.add_vec(self.r, delta))
    
    def translate(self, delta):
        self.set_t(geo.add_vec(self.t, delta))
    
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
    
    def project_3d_to_2d(self, pts_3d):
        return geo.project(self.T, self.f, pts_3d)
    
    def project_2d_to_3d(self, pts_2d):
        return geo.reverse_project(np.linalg.inv(self.T), self.f, self.t[-1], pts_2d)
    
