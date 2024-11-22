# tính dãy fibonacy bằng phương pháp chia để trị, sau đó đưa bảng tính vào để tính cấc giá trị 
# của số fibonacy lớn

import concurrent.futures
import numpy as np

# Hàm tính ma trận Fibonacci bằng cách sử dụng lũy thừa ma trận
def matrix_mult(A, B):
    return np.dot(A, B)

def matrix_pow(M, n):
     # Ma trận đơn vị

    result = np.array([[1, 0], [0, 1]])     
    base = M
    while n > 0:
        if n % 2 == 1:
            result = matrix_mult(result, base)
        base = matrix_mult(base, base)
        n //= 2
    return result

def fibonacci_matrix(n):
    if n == 0:
        return 0
    F = np.array([[1, 1], [1, 0]])
    result = matrix_pow(F, n-1)
    return result[0, 0]

def main():
    n = 9999
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(fibonacci_matrix, n)
        result = future.result() 
    print(f"Fibonacci thứ {n}: {result}")

if __name__ == '__main__':
    main()
