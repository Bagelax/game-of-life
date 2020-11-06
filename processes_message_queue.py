from multiprocessing import Process, Queue, Event, Manager
from sys import stdout
from typing import List

import numpy as np


class Controller(Process):
    def __init__(self, state: np.ndarray, iteration_number, message_queue: Queue, result: dict):
        super(Controller, self).__init__()
        self.steps = [np.zeros(state.shape) for _ in range(iteration_number + 1)]
        self.steps[0] = state
        self.message_queue = message_queue
        self.shutdown = Event()
        self.result = result

    def run(self) -> None:
        while not self.shutdown.is_set():
            cur = self.message_queue.get()
            if cur == 'STOP':
                if not self.message_queue.empty():
                    raise Exception('Something is wrong, queue not empty')
                self.result['steps'] = self.steps
                self.shutdown.set()
            else:
                self.steps[cur[0]][cur[1]][cur[2]] = cur[3]


class Cell(Process):
    adjacent: List[Queue]

    def __init__(self, i, j, starting_state, iteration_number, controller_queue: Queue):
        super(Cell, self).__init__()
        self.message_queue = Queue()
        self.control_queue = controller_queue
        self.adjacent = []
        self.state = starting_state
        self.iteration_number = iteration_number
        self.j = j
        self.i = i

    def run(self) -> None:
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
                else:
                    states[cur[0] + 1] = False
                for msg_queue in self.adjacent:
                    msg_queue.put((cur[0] + 1, states[cur[0] + 1]))
                self.control_queue.put((cur[0] + 1, self.i, self.j, states[cur[0] + 1]))

                done_iterations += 1


def create_steps(width=20, height=20, starting_state='random', iteration_number=50):
    if isinstance(starting_state, str):
        state = (np.random.rand(width * height).reshape(width, height) > 0.5).astype(np.int8)
    else:
        height, width = starting_state.shape
        state = starting_state

    processes = [[None for _ in range(width)] for _ in range(height)]
    controller_queue = Queue()
    manager = Manager()
    result = manager.dict()
    controller = Controller(state, iteration_number, controller_queue, result)
    controller.start()

    for i in range(height):
        for j in range(width):
            processes[i][j] = Cell(i, j, state[i][j], iteration_number, controller_queue)

    for i in range(height):
        for j in range(width):
            # stdout.write(f'starting cell {i}, {j}\n')
            adjacent_cells = [(-1, -1), (-1, 0), (-1, 1),
                              (0,  -1),          (0,  1),
                              (1,  -1), (1,  0), (1,  1)]
            processes[i][j].adjacent = [processes[(i + x[0]) % height][(j + x[1]) % width].message_queue
                                        for x in adjacent_cells]
            processes[i][j].start()

    for i in range(height):
        for j in range(width):
            # stdout.write(f'waiting for cell {i}, {j}\n')
            processes[i][j].join()

    controller_queue.put("STOP")

    controller.join()

    return result['steps']
