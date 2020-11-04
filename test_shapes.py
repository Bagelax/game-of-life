import numpy as np


def block():
    ret = np.zeros((4, 4))
    ret[1][1] = True
    ret[1][2] = True
    ret[2][1] = True
    ret[2][2] = True

    return ret


def blinker():
    ret = np.zeros((5, 5))
    ret[2][1] = True
    ret[2][2] = True
    ret[2][3] = True

    return ret


def pulsar():
    ret = np.zeros((17, 17))

    ret[2][4] = True
    ret[2][5] = True
    ret[2][6] = True
    ret[2][10] = True
    ret[2][11] = True
    ret[2][12] = True
    ret[4][2] = True
    ret[4][7] = True
    ret[4][9] = True
    ret[4][14] = True
    ret[5][2] = True
    ret[5][7] = True
    ret[5][9] = True
    ret[5][14] = True
    ret[6][2] = True
    ret[6][7] = True
    ret[6][9] = True
    ret[6][14] = True
    ret[7][4] = True
    ret[7][5] = True
    ret[7][6] = True
    ret[7][10] = True
    ret[7][11] = True
    ret[7][12] = True
    ret[9][4] = True
    ret[9][5] = True
    ret[9][6] = True
    ret[9][10] = True
    ret[9][11] = True
    ret[9][12] = True
    ret[10][2] = True
    ret[10][7] = True
    ret[10][9] = True
    ret[10][14] = True
    ret[11][2] = True
    ret[11][7] = True
    ret[11][9] = True
    ret[11][14] = True
    ret[12][2] = True
    ret[12][7] = True
    ret[12][9] = True
    ret[12][14] = True
    ret[14][4] = True
    ret[14][5] = True
    ret[14][6] = True
    ret[14][10] = True
    ret[14][11] = True
    ret[14][12] = True

    return ret


def glider():
    ret = np.zeros((30, 30))
    ret[1][1] = True
    ret[3][1] = True
    ret[2][2] = True
    ret[2][3] = True
    ret[3][2] = True

    return ret
