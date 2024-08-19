import numpy as np

def project(T, f : float, pts_3d : list) -> list:
    X = np.array(pts_3d).T
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

