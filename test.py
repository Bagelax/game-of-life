from test_shapes import pulsar, blinker, glider
from threads_keys_and_semaphores import create_steps as create_steps_1
from threads_message_queue import create_steps as create_steps_2
from processes_message_queue import create_steps as create_steps_3

if __name__ == '__main__':
    a = create_steps_3(starting_state=pulsar(), iteration_number=135)
    # a = create_steps_3()
    print(a)
