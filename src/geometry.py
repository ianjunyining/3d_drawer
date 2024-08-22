import numpy as np
import math

def project(T, f : float, pts_3d : list) -> list:
    # print("pts_3d: ", pts_3d)
    X = np.array(pts_3d).T
    # print("X: ", X)
    X1 = np.dot(T, X)
    U = f * X1[0, :] / X1[2, :]
    V = f * X1[1, :] / X1[2, :]
    # print("T: ", T)
    # print("f: ", f)
    # print("X: ", X)
    # print("X1: ", X1)
    # print("U: ", U)
    # print("V: ", V)
    return [(u, v) for u, v in zip(U, V)]

def reverse_project(T_inv, f : float, z: float, pts_2d : list):
    scale = z / f
    U = np.array(pts_2d).T
    X1 = np.ones((4, len(pts_2d)))
    X1[0, :] = U[0, :] * scale
    X1[1, :] = U[1, :] * scale
    X1[2, :] = z
    X = np.dot(T_inv, X1)
    pts_3d = []
    for i in range(X.shape[1]):
        pts_3d.append([X[0, i], X[1, i], X[2, i], X[3, i]])
    return pts_3d

def distance_3d(pt1, pt2):
    x1, y1, z1 = pt1[0:3]
    x2, y2, z2 = pt2[0:3]
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)

def add_vec(v1, v2):
    return [i1 + i2 for i1, i2 in zip(v1, v2)]

def points_boundary(points):
    X = [point[0] for point in points]
    Y = [point[1] for point in points]
    return min(X), max(X), min(Y), max(Y)

def point_in_boundary(min_x, max_x, min_y, max_y , point):
    return point[0] >= min_x and point[0] <= max_x \
        and point[1] >= min_y and point[1] <= max_y

def translate_point_3D(point : tuple, delta : tuple):
    return (point[0] + delta[0], point[1] + delta[1], point[2] + delta[2], 1)

def  translate_points_3D(points : list, delta : tuple):
    return [translate_point_3D(pt, delta) for pt in points]

def avg_points3D(points):
    sum0, sum1, sum2 = 0, 0
    for point in points:
        sum0 += point[0]
        sum1 += point[1]
        sum2 += point[2]
    n = len(points)
    return (sum0 / n, sum1 / n, sum2 / n, 1)
