import multiprocessing

# chia ma trận lớn thành 4 ma trận nhr hơn
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

A = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 16]
]

B = [
    [16, 15, 14, 13],
    [12, 11, 10, 9],
    [8, 7, 6, 5],
    [4, 3, 2, 1]
]

# Nhân hai ma trận song song
C = parallel_multiply_matrices(A, B)

# In kết quả
for row in C:
    print(row)