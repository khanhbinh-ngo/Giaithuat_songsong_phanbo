# CĂN BẢN VỀ GIẢI THUẬT TÍNH TOÁN PREFIX SUM SONG SONG

Trong thiết kế nhiều khi chúng ta sẽ gặp các biểu thức cộng dồn dưới dang
Y_0 = A_0
Y_1 = A_0 + A_1
Y_2 = A_0 + A_1 + A_2

Những tổng cộng dồn này (Y_0, Y_1, Y_2, ...) được gọi là các prefix (gọi tắt là các prefix sum) có thể được tính một cách song song trong log N bước sử dụng một cấu trúc gọi là cây prefix. Kỹ thuật này nói chung được gọi là giải thuật tính prefix song song (parallel-prefix algorithm).

Như trên ta có thể thấy được rằng với nó có 
+ Độ phức tạp của work là O(n log n) 
+ Độ phức tạp của Depth là O(log n)

- Đây cũng là cách sử dụng nhiều nhất trong việc thiết kế thuật toán song song
- Có thể dùng chúng trong việc giải quyết các bài toán giống nhau với các phép toán mã nhị phân (nói nôm na là có thẻ sử dụng để có thể thiết kế vào các mahcj logic và một số bộ chuyển đổi tương đương)

Có 2 thuật toán khác được sử dụng :
Chia để trị
> Chia để trị sẽ chia bài toán cần giải thành các bài toán nhỏ hơn - thuwognf là chia đôi
> sau đó giải quyết chúng một cách song song
> Cuối cùng là gộp kết quả

### Đây là mã giả của thuật toans chia để trị

function scan_r(A, B, s, t, offset){
    if s=t-1 then{
        B[s] = offset + A[s];
        return;
    }
    mid = (s+t)/2;
    in parallel:
    scan_r(A, B, s, mid, offset);
    scan_r(A, B, mid, t, offset + leftsum)
}
function scan(A, B){
    call reduce(A, n) and save the reduce tree;
    scan_r(A, B, 0, n, 0);
}
            
Giải quyết nửa trái và nửa phải xong rồi hợp lại với nhau 