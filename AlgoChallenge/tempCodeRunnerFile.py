def matrix_multiply(A, B, mod=None):
    """Nhân hai ma trận A và B. Nếu mod không phải None, thực hiện modulo."""
    return [
        [
            (A[0][0] * B[0][0] + A[0][1] * B[1][0]) % mod if mod else A[0][0] * B[0][0] + A[0][1] * B[1][0],
            (A[0][0] * B[0][1] + A[0][1] * B[1][1]) % mod if mod else A[0][0] * B[0][1] + A[0][1] * B[1][1]
        ],
        [
            (A[1][0] * B[0][0] + A[1][1] * B[1][0]) % mod if mod else A[1][0] * B[0][0] + A[1][1] * B[1][0],
            (A[1][0] * B[0][1] + A[1][1] * B[1][1]) % mod if mod else A[1][0] * B[0][1] + A[1][1] * B[1][1]
        ]
    ]


def matrix_exponentiation(matrix, n, mod=None):
    """Tính lũy thừa ma trận matrix^n với n >= 0."""
    result = [[1, 0], [0, 1]]  # Ma trận đơn vị
    base = matrix

    while n > 0:
        if n % 2 == 1:
            result = matrix_multiply(result, base, mod)
        base = matrix_multiply(base, base, mod)
        n //= 2

    return result


def fibonacci(n, mod=None):
    """Tính số Fibonacci thứ n bằng ma trận lũy thừa."""
    if n == 0:
        return 0
    if n == 1:
        return 1

    F = [[1, 1], [1, 0]]
    result = matrix_exponentiation(F, n - 1, mod)
    return result[0][0]  # F(n) nằm ở vị trí (0,0) trong ma trận


def process_queries(queries, mod=None):
    """Xử lý danh sách các truy vấn Fibonacci."""
    return [fibonacci(q, mod) for q in queries]


def MAIN(filename='input.txt'):
    with open(filename, 'r') as file:
        data = file.readlines()
                                                            
    N, Q = map(int, data[0].strip().split())
    queries = [int(data[i].strip()) for i in range(1, N + 1)]

    # Xử lý các truy vấn
    results = process_queries(queries)
    return results

