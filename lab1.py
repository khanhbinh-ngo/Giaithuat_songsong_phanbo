import multiprocessing

# chia ma trận lớn thành 4 ma trận nhỏ hơn
def divide_matrix(A):
    
    n = len(A)
    mid = n // 2
    A11 = [row[:mid] for row in A[:mid]]
    A12 = [row[mid:] for row in A[:mid]]
    A21 = [row[:mid] for row in A[mid:]]
    A22 = [row[mid:] for row in A[mid:]]
    return A11, A12, A21, A22

# Hàm cộng hai ma trận
def add_matrices(A, B):
    n = len(A)
    return [[A[i][j] + B[i][j] for j in range(n)] for i in range(n)]

# Hàm nhân hai ma trận con
def multiply_matrices(A, B):
    n = len(A)
    C = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

# Hàm kết hợp các ma trận con thành ma trận lớn
def combine_matrices(C11, C12, C21, C22):
    n = len(C11) * 2
    result = [[0 for _ in range(n)] for _ in range(n)]
    
    for i in range(len(C11)):
        for j in range(len(C11)):
            result[i][j] = C11[i][j]
            result[i][j + len(C11)] = C12[i][j]
            result[i + len(C11)][j] = C21[i][j]
            result[i + len(C11)][j + len(C11)] = C22[i][j]
    
    return result

# Hàm xử lý song song với 4 core
def parallel_multiply_matrices(matrix_a, matrix_b):
    # Chia ma trận A và B thành các phần con
    A11, A12, A21, A22 = divide_matrix(matrix_a)
    B11, B12, B21, B22 = divide_matrix(matrix_b)
    
    # Khởi tạo pool với 4 core
    with multiprocessing.Pool(processes=4) as pool:
        # Tính toán song song cho các phần tử của ma trận kết quả
        C11 = pool.apply_async(add_matrices, (multiply_matrices(A11, B11), multiply_matrices(A12, B21)))
        C12 = pool.apply_async(add_matrices, (multiply_matrices(A11, B12), multiply_matrices(A12, B22)))
        C21 = pool.apply_async(add_matrices, (multiply_matrices(A21, B11), multiply_matrices(A22, B21)))
        C22 = pool.apply_async(add_matrices, (multiply_matrices(A21, B12), multiply_matrices(A22, B22)))

        # Lấy kết quả từ các tiến trình song song
        result_C11 = C11.get()
        result_C12 = C12.get()
        result_C21 = C21.get()
        result_C22 = C22.get()
    
    return combine_matrices(result_C11, result_C12, result_C21, result_C22)
## =================================================================================

import numpy as np
import time
from multiprocessing import Pool
import multiprocessing

def matrix_multiply(matrix_a, matrix_b):
    # Get the dimensions of the input matrices
    m, n = matrix_a.shape
    n, p = matrix_b.shape

    # Initialize the result matrix with zeros
    result = np.zeros((m, p))

    # Perform matrix multiplication
    for i in range(m):
        for j in range(p):
            for k in range(n):
                result[i, j] += matrix_a[i, k] * matrix_b[k, j]

    return result
# import threading
# def matrix_multiply(matrix_a, matrix_b):
#     # Get the dimensions of the input matrices
#     m, n = matrix_a.shape
#     n, p = matrix_b.shape

#     # Initialize the result matrix with zeros
#     result = np.zeros((m, p))

#     # Create a list to store the threads
#     threads = []

#     def multiply_row(i):
#         for j in range(p):
#             for k in range(n):
#                 result[i, j] += matrix_a[i, k] * matrix_b[k, j]

#     # Create and start a thread for each row
#     for i in range(m):
#         thread = threading.Thread(target=multiply_row, args=(i,))
#         thread.start()
#         threads.append(thread)

#     # Wait for all threads to finish
#     for thread in threads:
#         thread.join()

#     return result

def pad_to_power_of_2(matrix):
    original_size = matrix.shape[0]
    next_power_of_2 = 2 ** (original_size - 1).bit_length()
    
    if original_size == next_power_of_2:
        return matrix  # No padding needed
    
    pad_size = next_power_of_2 - original_size
    padded_array = np.zeros((original_size + 1,  original_size + 1), dtype=matrix.dtype)
    padded_array[:original_size, :original_size] = matrix
    return padded_array

def remove_padding(padded_matrix, original_size):
    return padded_matrix[:original_size, :original_size]

def strassen_multiply(matrix_a, matrix_b):
    ori = matrix_a.shape[0]
    if matrix_a.shape[0] % 2 != 0 and matrix_a.shape[0]>4:
        #return np.dot(matrix_a, matrix_b)
        #return matrix_a @ matrix_b
        #return matrix_multiply(matrix_a, matrix_b)
        matrix_a = pad_to_power_of_2(matrix_a)
        matrix_b = pad_to_power_of_2(matrix_b)
    n = matrix_a.shape[0] // 2

    if n <= 4:
        return matrix_multiply(matrix_a, matrix_b)

    a11, a12, a21, a22 = matrix_a[:n, :n], matrix_a[:n, n:], matrix_a[n:, :n], matrix_a[n:, n:]
    b11, b12, b21, b22 = matrix_b[:n, :n], matrix_b[:n, n:], matrix_b[n:, :n], matrix_b[n:, n:]

    p1 = strassen_multiply(a11 + a22, b11 + b22)
    p2 = strassen_multiply(a21 + a22, b11)
    p3 = strassen_multiply(a11, b12 - b22)
    p4 = strassen_multiply(a22, b21 - b11)
    p5 = strassen_multiply(a11 + a12, b22)
    p6 = strassen_multiply(a21 - a11, b11 + b12)
    p7 = strassen_multiply(a12 - a22, b21 + b22)

    c11 = p1 + p4 - p5 + p7
    c12 = p3 + p5
    c21 = p2 + p4
    c22 = p1 - p2 + p3 + p6

    result = np.vstack((np.hstack((c11, c12)), np.hstack((c21, c22))))

    result = remove_padding(result, ori)
    return result

def parallel_multiply_matrices(matrix_a, matrix_b):
    ori = matrix_a.shape[0]
    if matrix_a.shape[0] % 2 != 0 and matrix_a.shape[0] > 4:
        matrix_a = pad_to_power_of_2(matrix_a)
        matrix_b = pad_to_power_of_2(matrix_b)

    if matrix_a.shape[0] <= 4:
        return matrix_multiply(matrix_a, matrix_b)
    mod = matrix_a.shape[0]
    blocks = []
    n = matrix_a.shape[0] // 2
    a11, a12, a21, a22 = matrix_a[:n, :n], matrix_a[:n, n:], matrix_a[n:, :n], matrix_a[n:, n:]
    b11, b12, b21, b22 = matrix_b[:n, :n], matrix_b[:n, n:], matrix_b[n:, :n], matrix_b[n:, n:]

    blocks.append((a11 + a22, b11 + b22))
    blocks.append((a21 + a22, b11))
    blocks.append((a11, b12 - b22))
    blocks.append((a22, b21 - b11))
    blocks.append((a11 + a12, b22))
    blocks.append((a21 - a11, b11 + b12))
    blocks.append((a12 - a22, b21 + b22))

    pool = multiprocessing.Pool()
    results = pool.starmap(strassen_multiply, blocks)
    pool.close()
    pool.join()

    c11 = results[0] + results[3] - results[4] + results[6]
    c12 = results[2] + results[4]
    c21 = results[1] + results[3]
    c22 = results[0] - results[1] + results[2] + results[5]

    result = np.vstack((np.hstack((c11, c12)), np.hstack((c21, c22))))
    result = remove_padding(result, ori)
    return result.astype(int)

if __name__ == '_main_':
    n = 500
    matrix_a = np.random.randint(0, 10, size=(n, n))
    print(matrix_a)
    matrix_b = np.random.randint(0, 10, size=(n, n))
    print(matrix_b)

    start = time.time()
    result = parallel_multiply_matrices(matrix_a, matrix_b)
    end = time.time()
    
    #result = remove_padding(result, (n, n))
    
    print("Time taken:", end - start)
    print(result)

# Nhân hai ma trận song song
C = parallel_multiply_matrices(A, B)

# In kết quả
for row in C:
    print(row)
import numpy as np
import time
from multiprocessing import Pool
import multiprocessing

def matrix_multiply(matrix_a, matrix_b):
    # Get the dimensions of the input matrices
    m, n = matrix_a.shape
    n, p = matrix_b.shape

    # Initialize the result matrix with zeros
    result = np.zeros((m, p))

    # Perform matrix multiplication
    for i in range(m):
        for j in range(p):
            for k in range(n):
                result[i, j] += matrix_a[i, k] * matrix_b[k, j]

    return result
# import threading
# def matrix_multiply(matrix_a, matrix_b):
#     # Get the dimensions of the input matrices
#     m, n = matrix_a.shape
#     n, p = matrix_b.shape

#     # Initialize the result matrix with zeros
#     result = np.zeros((m, p))

#     # Create a list to store the threads
#     threads = []

#     def multiply_row(i):
#         for j in range(p):
#             for k in range(n):
#                 result[i, j] += matrix_a[i, k] * matrix_b[k, j]

#     # Create and start a thread for each row
#     for i in range(m):
#         thread = threading.Thread(target=multiply_row, args=(i,))
#         thread.start()
#         threads.append(thread)

#     # Wait for all threads to finish
#     for thread in threads:
#         thread.join()

#     return result

def pad_to_power_of_2(matrix):
    original_size = matrix.shape[0]
    next_power_of_2 = 2 ** (original_size - 1).bit_length()
    
    if original_size == next_power_of_2:
        return matrix  # No padding needed
    
    pad_size = next_power_of_2 - original_size
    padded_array = np.zeros((original_size + 1,  original_size + 1), dtype=matrix.dtype)
    padded_array[:original_size, :original_size] = matrix
    return padded_array

def remove_padding(padded_matrix, original_size):
    return padded_matrix[:original_size, :original_size]

def strassen_multiply(matrix_a, matrix_b):
    ori = matrix_a.shape[0]
    if matrix_a.shape[0] % 2 != 0 and matrix_a.shape[0]>4:
        #return np.dot(matrix_a, matrix_b)
        #return matrix_a @ matrix_b
        #return matrix_multiply(matrix_a, matrix_b)
        matrix_a = pad_to_power_of_2(matrix_a)
        matrix_b = pad_to_power_of_2(matrix_b)
    n = matrix_a.shape[0] // 2

    if n <= 4:
        return matrix_multiply(matrix_a, matrix_b)

    a11, a12, a21, a22 = matrix_a[:n, :n], matrix_a[:n, n:], matrix_a[n:, :n], matrix_a[n:, n:]
    b11, b12, b21, b22 = matrix_b[:n, :n], matrix_b[:n, n:], matrix_b[n:, :n], matrix_b[n:, n:]

    p1 = strassen_multiply(a11 + a22, b11 + b22)
    p2 = strassen_multiply(a21 + a22, b11)
    p3 = strassen_multiply(a11, b12 - b22)
    p4 = strassen_multiply(a22, b21 - b11)
    p5 = strassen_multiply(a11 + a12, b22)
    p6 = strassen_multiply(a21 - a11, b11 + b12)
    p7 = strassen_multiply(a12 - a22, b21 + b22)

    c11 = p1 + p4 - p5 + p7
    c12 = p3 + p5
    c21 = p2 + p4
    c22 = p1 - p2 + p3 + p6

    result = np.vstack((np.hstack((c11, c12)), np.hstack((c21, c22))))

    result = remove_padding(result, ori)
    return result

def parallel_multiply_matrices(matrix_a, matrix_b):
    ori = matrix_a.shape[0]
    if matrix_a.shape[0] % 2 != 0 and matrix_a.shape[0] > 4:
        matrix_a = pad_to_power_of_2(matrix_a)
        matrix_b = pad_to_power_of_2(matrix_b)

    if matrix_a.shape[0] <= 4:
        return matrix_multiply(matrix_a, matrix_b)
    mod = matrix_a.shape[0]
    blocks = []
    n = matrix_a.shape[0] // 2
    a11, a12, a21, a22 = matrix_a[:n, :n], matrix_a[:n, n:], matrix_a[n:, :n], matrix_a[n:, n:]
    b11, b12, b21, b22 = matrix_b[:n, :n], matrix_b[:n, n:], matrix_b[n:, :n], matrix_b[n:, n:]

    blocks.append((a11 + a22, b11 + b22))
    blocks.append((a21 + a22, b11))
    blocks.append((a11, b12 - b22))
    blocks.append((a22, b21 - b11))
    blocks.append((a11 + a12, b22))
    blocks.append((a21 - a11, b11 + b12))
    blocks.append((a12 - a22, b21 + b22))

    pool = multiprocessing.Pool()
    results = pool.starmap(strassen_multiply, blocks)
    pool.close()
    pool.join()

    c11 = results[0] + results[3] - results[4] + results[6]
    c12 = results[2] + results[4]
    c21 = results[1] + results[3]
    c22 = results[0] - results[1] + results[2] + results[5]

    result = np.vstack((np.hstack((c11, c12)), np.hstack((c21, c22))))
    result = remove_padding(result, ori)
    return result.astype(int)

if _name_ == '_main_':
    n = 500
    matrix_a = np.random.randint(0, 10, size=(n, n))
    print(matrix_a)
    matrix_b = np.random.randint(0, 10, size=(n, n))
    print(matrix_b)

    start = time.time()
    result = parallel_multiply_matrices(matrix_a, matrix_b)
    end = time.time()
    
    #result = remove_padding(result, (n, n))
    
    print("Time taken:", end - start)
    print(result)