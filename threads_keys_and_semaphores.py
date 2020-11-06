from sys import stdout
from threading import Semaphore, Thread, Lock, Condition
from typing import List

import numpy as np

state: np.ndarray
state_locks: List[List[Lock]]
steps: List[np.ndarray]
read_semaphores: List[List[Semaphore]]
threads: List[List[Thread]]
remaining_writes: int
remaining_writes_lock: Condition


def cell(pos_x, pos_y, width, height, iteration_number):
    global state, read_semaphores, threads, steps, remaining_writes, state_locks, remaining_writes_lock

    for it_num in range(1, iteration_number + 1):
        counter = 0
        adjacent_cells = [(-1, -1), (-1, 0), (-1, 1),
                          (0,  -1),          (0,  1),
                          (1,  -1), (1,  0), (1,  1)]

        current = 0
        while len(adjacent_cells) > 0:
            i = (pos_y + adjacent_cells[current][0]) % height
            j = (pos_x + adjacent_cells[current][1]) % width
            if state_locks[i][j].acquire(blocking=False):
                counter += state[i][j]
                state_locks[i][j].release()
                read_semaphores[i][j].release()
                adjacent_cells.pop(current)
                current = 0
            else:
                current = current + 1 % len(adjacent_cells)

        for _ in range(8):
            read_semaphores[pos_y][pos_x].acquire()

        if counter == 3 or (counter == 2 and state[pos_y][pos_x]):
            state[pos_y][pos_x] = True
            steps[it_num][pos_y][pos_x] = True
        else:
            state[pos_y][pos_x] = False
            steps[it_num][pos_y][pos_x] = False

        remaining_writes_lock.acquire()
        remaining_writes -= 1
        if remaining_writes == 0:
            remaining_writes = width * height
            # stdout.write(f'finished iteration {it_num}\n')
            remaining_writes_lock.notifyAll()
        else:
            remaining_writes_lock.wait()
        remaining_writes_lock.release()


def create_steps(width=20, height=20, starting_state='random', iteration_number=50):
    global state, read_semaphores, threads, steps, remaining_writes, state_locks, remaining_writes_lock

    remaining_writes_lock = Condition()
    if isinstance(starting_state, str):
        state = (np.random.rand(width * height).reshape(width, height) > 0.5).astype(np.int8)
    else:
        height, width = starting_state.shape
        state = starting_state

    steps = [np.zeros((height, width)) for _ in range(iteration_number + 1)]
    steps[0] = starting_state

    read_semaphores = [[Semaphore(0) for _ in range(width)] for _ in range(height)]
    test = [[False for _ in range(width)] for _ in range(height)]
    state_locks = [[Lock() for _ in range(width)] for _ in range(height)]
    remaining_writes = width * height

    threads = [[None for _ in range(width)] for _ in range(height)]

    for i in range(height):
        for j in range(width):
            # stdout.write(f'starting cell {i}, {j}\n')
            threads[i][j] = Thread(target=cell, args=(i, j, width, height, iteration_number))
            threads[i][j].start()

    for i in range(height):
        for j in range(width):
            # stdout.write(f'waiting for cell {i}, {j}\n')
            threads[i][j].join()

    return steps
