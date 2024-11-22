# Nhân 2 ma trận vuông lớn
# 
# Mô tả ý tưởng bài toán nhân 2 ma trận vuông lớn:
# Ta chia nhỏ ma trận vuông lớn thành các ma trận vuông nhỏ hơn (cụ thể ta chia từng ma trận vuông lớn thành 4 ma trận vuông nhỏ hơn (nếu chia ra không phải là một ma trận vuông liền 
# sử dụng thêm 1 hàng hoặc một cột có giá trị 0 vào trong ma trận để tạo thành một ma trận vuông nhỏ hơn
# chia đến khi nào ma trận vuông chỉ còn lại các ma trận vuông 2x2, sau đó từng 4 ma trận vuông nhân với nhau
# sau khi thực hiện tuần tự, ta sẽ gộp các ma trận kết quả lại với nhau
# 
# Trieenr khai chi tiết thuật toán
# 
# Bước 1: chia ma trận lớn thành các ma trận con: để hỗ trợ chia để trị, chúng ta sẽ xây dựng hàm split_matrix() để chia một ma 
# trận thành 4 ma trận con (hay các khối con)
# 
# BƯớc 2: Nhân các ma trận song song: sử dụng hàm multiprocessing.Pool để xử lý hợp đồng thời các phép nhân trên các khối con của ma trận
# 
# Bước 3: Hợp nhất kết quả từ các ma trận con: xây dựng hàm combine_matrices để hợp nhất các ma trận con thành ma trận kết quả cuối cùng
# 
# Bước 4: xuất ra thời gian thực hiện thuật toán#

import multiprocessing as mp
import time
import threading
def add_matrices(A, B):
    n = len(A)
    return [[A[i][j] + B[i][j] for j in range(n)] for i in range(n)]

def subtract_matrices(A, B):
    """Trừ hai ma trận cùng kích thước."""
    n = len(A)
    return [[A[i][j] - B[i][j] for j in range(n)] for i in range(n)]

def serial_multiply_matrices(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def split_matrix(matrix):
    n = len(matrix)
    mid = n // 2
    A11 = [row[:mid] for row in matrix[:mid]]
    A12 = [row[mid:] for row in matrix[:mid]]
    A21 = [row[:mid] for row in matrix[mid:]]
    A22 = [row[mid:] for row in matrix[mid:]]
    return A11, A12, A21, A22

def join_matrices(C11, C12, C21, C22):
    n = len(C11)
    result = [[0] * (2 * n) for _ in range(2 * n)]
    for i in range(n):
        for j in range(n):
            result[i][j] = C11[i][j]
            result[i][j + n] = C12[i][j]
            result[i + n][j] = C21[i][j]
            result[i + n][j + n] = C22[i][j]
    return result

def parallel_multiply_matrices(A, B, depth=0, max_depth=2):
    n = len(A)

    if n <= 64 or depth >= max_depth:
        return serial_multiply_matrices(A, B)
    

    A11, A12, A21, A22 = split_matrix(A)
    B11, B12, B21, B22 = split_matrix(B)


    with mp.Pool(processes=4) as pool:
        # Các phép tính của Strassen
        M1 = pool.apply_async(parallel_multiply_matrices, (add_matrices(A11, A22), add_matrices(B11, B22), depth + 1))
        M2 = pool.apply_async(parallel_multiply_matrices, (add_matrices(A21, A22), B11, depth + 1))
        M3 = pool.apply_async(parallel_multiply_matrices, (A11, subtract_matrices(B12, B22), depth + 1))
        M4 = pool.apply_async(parallel_multiply_matrices, (A22, subtract_matrices(B21, B11), depth + 1))
        M5 = pool.apply_async(parallel_multiply_matrices, (add_matrices(A11, A12), B22, depth + 1))
        M6 = pool.apply_async(parallel_multiply_matrices, (subtract_matrices(A21, A11), add_matrices(B11, B12), depth + 1))
        M7 = pool.apply_async(parallel_multiply_matrices, (subtract_matrices(A12, A22), add_matrices(B21, B22), depth + 1))

        # Lấy kết quả từ các tiến trình
        M1, M2, M3, M4, M5, M6, M7 = M1.get(), M2.get(), M3.get(), M4.get(), M5.get(), M6.get(), M7.get()

    # Tính toán các khối con của C
    C11 = add_matrices(subtract_matrices(add_matrices(M1, M4), M5), M7)
    C12 = add_matrices(M3, M5)
    C21 = add_matrices(M2, M4)
    C22 = add_matrices(subtract_matrices(add_matrices(M1, M3), M2), M6)
    return join_matrices(C11, C12, C21, C22)



if __name__ == "__main__":
    # Định nghĩa kích thước ma trận
    n = 128
    matrix_a = [[1 for _ in range(n)] for _ in range(n)]
    matrix_b = [[1 for _ in range(n)] for _ in range(n)]

    # Bắt đầu tính toán thời gian
    start_time = time.time()
    
    # Nhân hai ma trận song song
    result = parallel_multiply_matrices(matrix_a, matrix_b)

    # Tính toán thời gian hoàn tất
    end_time = time.time()
    print(f"Time in executed {n}x{n}: {end_time - start_time} second")
