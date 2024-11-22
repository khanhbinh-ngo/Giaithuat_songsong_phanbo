import time
from prefix_sum import parallel_prefix_sum
import random

if __name__ == '_main_':
    
# Tạo mảng với 10,000 phần tử từ 0 đến 9999
#   arr = list(range(10000))
    arr = [random.randint(0,9) for _ in range(100)]
    print(arr)
# Đo thời gian thực hiện
    start_time = time.time()
    result = parallel_prefix_sum(arr)
    end_time = time.time()

# In kết quả
    print("Thời gian thực hiện:", end_time - start_time, "giây")
    print("Phần tử thứ 9000 của mảng prefix sum là:", result[90])