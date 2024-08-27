import sys
sys.path.insert(0, "/Users/ian/Documents/work/python/3d_drawer")
print(sys.path)

import unittest as ut
import numpy as np
import math
import src.geometry as geo

class TestGeo(ut.TestCase):

    def compare_tuple_list(self, l1, l2):
        self.assertEqual(len(l1), len(l2))
        for i1, i2 in zip(l1, l2):
            self.assertEqual(len(i1), len(i2))
            for j1, j2 in zip(i1, i2):
                self.assertEqual(j1, j2)
                
    def test_projection1(self):
        P = np.eye(4)
        P[2, 3] = 10
        pts = [(0, 0, 0, 1), (50, 50, 0, 1)]
        result = geo.project(P, 10, pts)
        expected = [
            (0, 0),
            (50, 50),
        ]
        self.compare_tuple_list(result, expected)

    def test_projection2(self):
        P = np.array([
            [0, -1, 0, 3],
            [1, 0, 0, 3],
            [0, 0, 1, 3],
            [0, 0, 0, 1],
        ])
        pts = [(1, 0, 2, 1), (0, 1, 2, 1)]
        result = geo.project(P, 2.5, pts)
        expected = [
            (1.5, 2),
            (1, 1.5),
        ]
        self.compare_tuple_list(result, expected)

    def test_reverse_projection(self):
        f = 2.5
        z = 3
        T = np.array([
            [0, -1, 0, 3],
            [1, 0, 0, 3],
            [0, 0, 1, z],
            [0, 0, 0, 1],
        ])
        pts_3d = [(0, 0, 0, 1), (10, 10, 0, 1)]
        pts_2d = geo.project(T, f, pts_3d)
        T_inv = np.linalg.inv(T)
        pts_3d_rev = geo.reverse_project(T_inv, f, z, pts_2d)
        self.compare_tuple_list(pts_3d_rev, pts_3d)

    def test_rotate_3D(self):
        result = geo.rotate_3D([[2, 0, 0, 1], [2, 2, 0, 1]], [0, 0, math.pi/2], [1, 1, 0])
        np.testing.assert_array_almost_equal(result, [[2, 2, 0, 1], [0, 2, 0, 1]])

if __name__ == "__main__":
    ut.main()