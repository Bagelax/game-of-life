from sys import stdout
from threading import Semaphore, Thread, Lock, Condition
from typing import List
import multiprocessing

import numpy as np

state: np.ndarray
steps: List[np.ndarray]
parts = 2
width = 4
height = 4


def cells(part):
    global state, height, width, parts
    ret = {}
    start = part * parts
    start_i = start // width * parts
    start_j = start % width

    # stdout.write(f"{start_i}, {start_j}\n")

    for i in range(start_i, start_i + parts):
        for j in range(start_j, start_j + parts):
            adjacent_cells = [(-1, -1), (-1, 0), (-1, 1),
                              (0,  -1),          (0,  1),
                              (1,  -1), (1,  0), (1,  1)]

            counter = 0
            for adjacent_cell in adjacent_cells:
                y = (i + adjacent_cell[0]) % height
                x = (j + adjacent_cell[1]) % width
                counter += state[y][x]

            # if i == 8 and j == 6:
            #     stdout.write(f'{counter}\n')

            if counter == 3 or (counter == 2 and state[i][j]):
                cur_state = 1
            else:
                cur_state = 0

            ret[i, j] = cur_state

    return ret


def create_steps(w=20, h=20, starting_state='random', iteration_number=50, part_edge_size=0):
    global state, steps, height, width, parts

    parts = part_edge_size

    if isinstance(starting_state, str):
        width = w
        height = h
        state = (np.random.rand(width * height).reshape(width, height) > 0.5).astype(np.int8)
    else:
        height, width = starting_state.shape
        state = starting_state

    if height % parts != 0 or width % parts != 0:
        raise Exception('Width and height must be dividable by part edge size')

    steps = [np.zeros((height, width)) for _ in range(iteration_number + 1)]
    steps[0] = np.copy(state)

    for i in range(iteration_number):
        with multiprocessing.Pool() as pool:
            pools = pool.map(cells, range(width // parts * height // parts))

            for ret_dict in pools:
                for x, y in ret_dict:
                    state[x][y] = ret_dict[x, y]
                    steps[i + 1][x][y] = ret_dict[x, y]

    return steps
