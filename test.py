from test_shapes import pulsar, blinker, glider
from threads_keys_and_semaphores import create_steps

if __name__ == '__main__':
    a = create_steps(starting_state=pulsar(), iteration_number=10)
    print(a)
