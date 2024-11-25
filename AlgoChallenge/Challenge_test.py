from multiprocessing import Pool

def matrix_multiply(A, B, mod=None):
    if mod:
        return [
            [
                (A[0][0] * B[0][0] + A[0][1] * B[1][0]) % mod,
                (A[0][0] * B[0][1] + A[0][1] * B[1][1]) % mod,
            ],
            [
                (A[1][0] * B[0][0] + A[1][1] * B[1][0]) % mod,
                (A[1][0] * B[0][1] + A[1][1] * B[1][1]) % mod,
            ],
        ]
    else:
        return [
            [
                A[0][0] * B[0][0] + A[0][1] * B[1][0],
                A[0][0] * B[0][1] + A[0][1] * B[1][1],
            ],
            [
                A[1][0] * B[0][0] + A[1][1] * B[1][0],
                A[1][0] * B[0][1] + A[1][1] * B[1][1],
            ],
        ]


def matrix_exponentiation(matrix, n, mod=None):
    result = [[1, 0], [0, 1]]
    base = matrix

    while n:
        if n & 1:
            result = matrix_multiply(result, base, mod)
        base = matrix_multiply(base, base, mod)
        n >>= 1

    return result


def fibonacci_large(n, mod=None):
    if n == 0:
        return 0
    if n == 1:
        return 1

    F = [[1, 1], [1, 0]]
    result = matrix_exponentiation(F, n - 1, mod)
    return result[0][0]


def compute_fibonacci_lookup(max_value, mod=None):
    """Tạo bảng Fibonacci chỉ lưu các giá trị lẻ."""
    fib_lookup = [0] * (max_value + 1)
    fib_lookup[1] = 1
    fib_lookup[2] = 1

    for i in range(3, max_value + 1):
        fib_lookup[i] = (fib_lookup[i - 1] + fib_lookup[i - 2]) % mod if mod else fib_lookup[i - 1] + fib_lookup[i - 2]

    return fib_lookup


def MAIN(filename='input.txt'):
    with open(filename, 'r') as file:
        data = file.readlines()

    N, Q = map(int, data[0].strip().split())
    queries = [int(data[i].strip()) for i in range(1, N + 1)]

    max_value = max(queries)

    # Tạo bảng Fibonacci hiệu quả
    fib_lookup = compute_fibonacci_lookup(max_value, mod)

    # Trả lời các truy vấn
    results = [fib_lookup[q] for q in queries]
    return results
if __name__ == "__main__":
    results = MAIN('AlgoChallenge\input.txt')
    print("\n".join(map(str, results)))
