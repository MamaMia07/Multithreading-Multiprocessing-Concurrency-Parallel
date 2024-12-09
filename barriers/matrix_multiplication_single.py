'''
matrix_A=[[3, 1, -4],
          [2, -3, 1],
          [5, -2, 8]]
matrix_B = [[1, -2, -1],
            [8, 5, 4],
            [-1, -2, 3]]
'''
import time
from random import Random

matrix_size = 200
matrix_A = [[0]* matrix_size for a in range(matrix_size)]
matrix_B = [[0]* matrix_size for b in range(matrix_size)]
result = [[0]* matrix_size for r in range(matrix_size)]

random = Random()

def generate_random_matrix(matrix):
    for row in range(matrix_size):
        for col in range(matrix_size):
            matrix[row][col] = random.randint(-5, 5)

start = time.time()
for t in range(10):
    generate_random_matrix(matrix_A)
    generate_random_matrix(matrix_B)
    result = [[0] * matrix_size for r in range(matrix_size)]
    for row in range(matrix_size):
        for col in range(matrix_size):
            for i in range(matrix_size):
                result[row][col] += matrix_A[row][i] * matrix_B[i][col]

end = time.time()
print("Done, time taken: ", end - start)
# for row in range(matrix_size):
#     print(matrix_A[row], matrix_B[row], result[row])
# print()