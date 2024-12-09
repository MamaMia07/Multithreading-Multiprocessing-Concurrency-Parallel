import multiprocessing
import time
from random import Random
from multiprocessing import Barrier, Process

process_count = 8 #(for 8 processors)
matrix_size = 5
random = Random()

'''The problem  deals with how process memory sharing works in Python.
We can only share variables and single dimensional array and to represent our matrix in our previous
implementation, we have used a two dimensional array.
So we need to map this two dimensional array into a single dimension array.'''



def generate_random_matrix(matrix):
    for row in range(matrix_size):
        for col in range(matrix_size):
            matrix[row* matrix_size + col] = random.randint(-5, 5)



def work_out_row(id, matrix_A, matrix_B, result, work_start, work_complete):
    # id is the number of the process
    while True:
        work_start.wait()
        for row in range(id, matrix_size, process_count):
            for col in range(matrix_size):
                for i in range(matrix_size):
                    result[row* matrix_size +col] += matrix_A[row* matrix_size + i] * matrix_B[i* matrix_size + col]
        work_complete.wait()

if __name__ == '__main__':

    multiprocessing.set_start_method('spawn')
    work_start = Barrier(process_count + 1)
    work_complete = Barrier(process_count + 1)

    matrix_A = multiprocessing.Array('i', [0]* (matrix_size * matrix_size), lock=False)
    matrix_B = multiprocessing.Array('i', [0] * (matrix_size * matrix_size), lock=False)
    result = multiprocessing.Array('i', [0] * (matrix_size * matrix_size), lock=False)

    for p in range(process_count):
        Process(target = work_out_row, args = (p, matrix_A, matrix_B, result, work_start, work_complete)).start()

    start = time.time()
    for t in range(10):
        generate_random_matrix(matrix_A)
        generate_random_matrix(matrix_B)
        for i in range(matrix_size * matrix_size):
            result[i] = 0
        work_start.wait()
        work_complete.wait()
        for r in range(matrix_size):
            for c in range(matrix_size):
                print(result[r * matrix_size + c], " ", end='')
            print('')
        print('')
    end = time.time()
    print("Done, time taken: ", end - start)

