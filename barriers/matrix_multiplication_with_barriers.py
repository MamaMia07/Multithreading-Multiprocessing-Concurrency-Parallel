import time
from random import Random
from threading import Barrier, Thread

matrix_size = 200
matrix_A = [[0]* matrix_size for a in range(matrix_size)]
matrix_B = [[0]* matrix_size for b in range(matrix_size)]
result = [[0]* matrix_size for r in range(matrix_size)]
random = Random()

#work_start  barrier signals that all the child threads can start working in the different rows together.
# count = matrix_size +1  because child threads(one thread per row) and the parent thread
work_start = Barrier(matrix_size+1)
work_complete = Barrier(matrix_size+1) #This will represent when each thread finishes their work

def generate_random_matrix(matrix):
    for row in range(matrix_size):
        for col in range(matrix_size):
            matrix[row][col] = random.randint(-5, 5)


# computation for row
def work_out_row(row):
    while True: # infinite loop - because we are calling this from a thread and we want to compute multiple matrices
        work_start.wait() #the barrier is the way the tread is signaled that there is a row to be computed.
        for col in range(matrix_size):
            for i in range(matrix_size):
                result[row][col] += matrix_A[row][i] * matrix_B[i][col]
        work_complete.wait()


for row in range(matrix_size):
    Thread(target = work_out_row, args = (row,)).start()

start = time.time()
for t in range(10):
    generate_random_matrix(matrix_A)
    generate_random_matrix(matrix_B)
    result = [[0] * matrix_size for r in range(matrix_size)]
    work_start.wait() # to tell all the threads that the matrices are ready for in the matrix multiplication to be computed.
    '''When this happens and all of our threads are waiting on the work to start, the barrier will unblock
        and each of the thread will work out each row.
        Then once it finishes, it will go on the work_complete barrier.'''
    work_complete.wait()

end = time.time()
print("Done, time taken: ", end - start)

'''t's not a huge improvement over what we have.
This is due to the python's global interpreter.
It doesn't let more than one tried to execute concurrently.'''