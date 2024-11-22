## Chạm khắc ánh sáng
#Bạn là một kỹ sư xử lý hình ảnh tại một công ty chuyên phát triển ứng dụng chỉnh sửa ảnh. Công ty đang nghiên cứu các hiệu ứng lọc mới để làm mịn, làm sắc nét hoặc tăng cường chi tiết cho ảnh. Bạn được giao nhiệm vụ áp dụng một bộ lọc (kernel) lên một bức ảnh nhất định để tạo ra một hiệu ứng đặc biệt. Hãy tính ma trận kết quả bằng cách thực hiện phép tích chập giữa ma trận của bức ảnh và kernel đã cho.

# Input:
# Dòng đầu tiên gồm 1 số nguyên 
#  là tổng số bức ảnh cần xử lí
# Trong 
#  cặp ma trận tiếp theo:
# - Dòng đầu tiên là 2 số nguyên 
# , lần lượt là kích thước của ma trận vuông biểu diễn ảnh và kernel.
# - 
#  dòng tiếp theo, với dòng 
#  gồm 
#  số nguyên 
#  biểu diễn một pixel ảnh.
# - 
#  dòng tiếp theo, với dòng 
#  gồm 
#  số nguyên 
#  biểu diễn giá trị của kernel.

# Output:
# Function MAIN(input_file) trả về 
#  ma trận số nguyên, là các ma trận biểu diễn ảnh sau khi được lọc bởi kernel.

# Ví dụ:
# Input:
# 1
# 5 3
# 66 71 86 41 55
# 0 9 11 84 134
# 87 154 216 0 94
# 47 16 55 1 84
# 0 0 0 84 1
# -1 0 1
# 0 1 0
# 1 0 -1

# Output:
# 57 60 11 -82 139
# -83 -100 135 175 93
# 80 157 306 94 11
# 201 145 -183 -122 168
# 16 8 -15 113 0
# # #