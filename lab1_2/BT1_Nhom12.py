import multiprocessing
import time
import random

def recursive_prefix_sum(arr, result, start=0):
    
    n = len(arr)
    if n <= 100:
        prefix_sum = [0] * n
        prefix_sum[0] = arr[0]
        for i in range(1, n):
            prefix_sum[i] = prefix_sum[i - 1] + arr[i]
        result[start:start + n] = prefix_sum
    else:
        # Chia mảng thành 2 phần và xử lý đệ quy
        mid = n // 2
        left_result = multiprocessing.Array('i', mid)
        right_result = multiprocessing.Array('i', n - mid)
        
        # Tạo 2 tiến trình cho 2 nửa
        left_process = multiprocessing.Process(target=recursive_prefix_sum, args=(arr[:mid], left_result, start))
        right_process = multiprocessing.Process(target=recursive_prefix_sum, args=(arr[mid:], right_result, start + mid))
        
        # Bắt đầu và chờ tiến trình kết thúc
        left_process.start()
        right_process.start()
        left_process.join()
        right_process.join()
        
        left_process.terminate()
        right_process.terminate()
        
        # Gộp kết quả với giá trị offset
        offset = left_result[-1]
        result[start:start + mid] = left_result[:]
        result[start + mid:start + n] = [x + offset for x in right_result[:]]

def parallel_prefix_sum(arr):
    n = len(arr)
    result = multiprocessing.Array('i', n)  
    
    # Kết quả sẽ lưu toàn bộ prefix sum
    # Thực hiện tính toán đệ quy với mảng đầu vào
    
    recursive_prefix_sum(arr, result)
    return result[:]

if __name__ == '_main_':
    
    arr = [random.randint(0, 9) for _ in range(10000)]
    print(arr)
    start_time = time.time()
    result = parallel_prefix_sum(arr)
    end_time = time.time()
    
    print("time in process", end_time - start_time)
    print("the 90th of prefix sum", result[9000]) 