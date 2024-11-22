import multiprocessing as mp

def parallel_prefix_sum(array):
    n = len(array)
    result = [0] * n
    num_processes = mp.cpu_count()
    
    # Copy array to shared memory for multiprocessing
    shared_array = mp.Array('i', array)
    shared_result = mp.Array('i', [0] * n)
    
    def up_sweep(start, end, stride):
        for i in range(start, end, stride * 2):
            if i + stride < n:
                shared_array[i + stride * 2 - 1] += shared_array[i + stride - 1]

    def down_sweep(start, end, stride):
        for i in range(start, end, stride * 2):
            if i + stride < n:
                temp = shared_array[i + stride - 1]
                shared_array[i + stride - 1] = shared_array[i + stride * 2 - 1]
                shared_array[i + stride * 2 - 1] += temp

    # Up-sweep phase
    stride = 1
    while stride < n:
        processes = []
        for i in range(0, n, stride * 2 * num_processes):
            p = mp.Process(target=up_sweep, args=(i, min(i + stride * 2 * num_processes, n), stride))
            processes.append(p)
            p.start()
        for p in processes:
            p.join()
        stride *= 2

    # Set the last element to 0 before the down-sweep phase
    if n > 0:
        shared_array[n - 1] = 0

    # Down-sweep phase
    stride = n // 2
    while stride > 0:
        processes = []
        for i in range(0, n, stride * 2 * num_processes):
            p = mp.Process(target=down_sweep, args=(i, min(i + stride * 2 * num_processes, n), stride))
            processes.append(p)
            p.start()
        for p in processes:
            p.join()
        stride //= 2

    # Copy results to final array
    for i in range(n):
        result[i] = shared_array[i]
    
    return result

# Example usage
if __name__ == "__main__":
    array = [1, 2, 3, 4, 5, 6, 7, 10 , 9, 20, 22, 1, 9, 8]
    result = parallel_prefix_sum(array)
    print("Original array:", array)
    print("Prefix sum:", result)
