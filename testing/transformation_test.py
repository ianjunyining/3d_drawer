import sys
sys.path.insert(0, "/Users/ian/Documents/work/python/3d_drawer")
print(sys.path)

import unittest as ut
import numpy as np
import src.transformation as trans
import math

class TestTransformation(ut.TestCase):
    def _test_transformation(self, r, t, expected_T):
        transformation = trans.Transformation(r, t)
        np.testing.assert_array_almost_equal(transformation.T, expected_T)

    def test_yaw(self):
        r = [0, 0, math.pi / 2]
        t = [1, 2, 3]
        expected_T = np.array([
            [0, -1, 0, 1],
            [1, 0, 0, 2],
            [0, 0, 1, 3],
            [0, 0, 0, 1]
        ])
        self._test_transformation(r, t, expected_T)

    def test_pitch(self):
        r = [0, math.pi / 2, 0]
        t = [1, 2, 3]
        expected_T = np.array([
            [0, 0, 1, 1],
            [0, 1, 0, 2],
            [-1, 0, 0, 3],
            [0, 0, 0, 1]
        ])
        self._test_transformation(r, t, expected_T)

    def test_roll(self):
        r = [math.pi / 2, 0, 0]
        t = [1, 2, 3]
        expected_T = np.array([
            [1, 0, 0, 1],
            [0, 0, -1, 2],
            [0, 1, 0, 3],
            [0, 0, 0, 1]
        ])
        self._test_transformation(r, t, expected_T)

    def test_yaw_pitch(self):
        r = [0, math.pi / 2, math.pi / 2]
        t = [1, 2, 3]
        expected_T = np.array([
            [0, -1, 0, 1],
            [0, 0, 1, 2],
            [-1, 0, 0, 3],
            [0, 0, 0, 1]
        ])
        self._test_transformation(r, t, expected_T)
    
    def test_pitch_roll(self):
        r = [math.pi / 2, math.pi / 2, 0]
        t = [1, 2, 3]
        expected_T = np.array([
            [0, 1, 0, 1],
            [0, 0, -1, 2],
            [-1, 0, 0, 3],
            [0, 0, 0, 1]
        ])
        self._test_transformation(r, t, expected_T)

if __name__ == "__main__":
    ut.main()

