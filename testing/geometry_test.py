import sys
sys.path.insert(0, "/Users/ian/Documents/work/python/3d_drawer")
print(sys.path)

import unittest as ut
import numpy as np
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

if __name__ == "__main__":
    ut.main()