from queue import PriorityQueue
from sys import stdout
from threading import Thread
from typing import List

import numpy as np

steps: List[np.ndarray]


class Cell(Thread):
    adjacent: List[PriorityQueue]

    def __init__(self, i, j, starting_state, iteration_number):
        Thread.__init__(self)
        self.message_queue = PriorityQueue()
        self.adjacent = []
        self.state = starting_state
        self.iteration_number = iteration_number
        self.j = j
        self.i = i

    def run(self) -> None:
        global steps

        for msg_queue in self.adjacent:
            msg_queue.put((0, self.state))

        done_iterations = 0
        sum_for_iter = [[0, 0] for _ in range(self.iteration_number + 1)]
        states = [0 for _ in range(self.iteration_number + 1)]
        states[0] = self.state
        while done_iterations < self.iteration_number:

            cur = self.message_queue.get()
            sum_for_iter[cur[0]][0] += 1
            sum_for_iter[cur[0]][1] += cur[1]

            if sum_for_iter[cur[0]][0] == 8:
                if sum_for_iter[cur[0]][1] == 3 or (sum_for_iter[cur[0]][1] == 2 and states[cur[0]]):
                    states[cur[0] + 1] = True
                    steps[cur[0] + 1][self.i][self.j] = True
                else:
                    states[cur[0] + 1] = False
                    steps[cur[0] + 1][self.i][self.j] = False
                for msg_queue in self.adjacent:
                    msg_queue.put((cur[0] + 1, states[cur[0] + 1]))

                done_iterations += 1


def create_steps(width=20, height=20, starting_state='random', iteration_number=50):
    global steps

    if isinstance(starting_state, str):
        state = (np.random.rand(width * height).reshape(width, height) > 0.5).astype(np.int8)
    else:
        height, width = starting_state.shape
        state = starting_state

    steps = [np.zeros((height, width)) for _ in range(iteration_number + 1)]
    steps[0] = state

    threads = [[None for _ in range(width)] for _ in range(height)]

    for i in range(height):
        for j in range(width):
            threads[i][j] = Cell(i, j, state[i][j], iteration_number)

    for i in range(height):
        for j in range(width):
            # stdout.write(f'starting cell {i}, {j}\n')
            adjacent_cells = [(-1, -1), (-1, 0), (-1, 1),
                              (0,  -1),          (0,  1),
                              (1,  -1), (1,  0), (1,  1)]
            threads[i][j].adjacent = [threads[(i + x[0]) % height][(j + x[1]) % width].message_queue
                                      for x in adjacent_cells]
            threads[i][j].start()

    for i in range(height):
        for j in range(width):
            # stdout.write(f'waiting for cell {i}, {j}\n')
            threads[i][j].join()

    return steps
