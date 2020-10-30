import numpy as np


def create_steps():
    n = 20
    steps = [(np.random.rand(n ** 2).reshape(n, n) > 0.5).astype(np.int8) for i in range(50)]
    return steps
