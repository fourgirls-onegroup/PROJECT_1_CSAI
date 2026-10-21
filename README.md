# 1. Giới thiệu dự án

## Tên dự án: Bloxorz

Bloxorz là trò chơi giải đố trong đó người chơi điều khiển một khối hình chữ nhật trên một hệ thống các ô gạch để đưa khối đến vị trí đích. Người chơi cần tính toán hướng di chuyển và trạng thái của khối để vượt qua từng màn chơi.

Trò chơi được xây dựng bằng Python và thư viện Ursina Engine, đồng thời tích hợp các thuật toán tìm kiếm để hỗ trợ giải màn chơi.

# 2. Phân loại màn chơi

Các màn chơi được chia thành 3 mức độ:

***EASY (Màn 1–4)***

* Các màn chơi cơ bản, được thiết kế để người chơi làm quen với:

* Cách điều khiển khối.

* Các trạng thái của khối.

* Luật di chuyển.

* Cách tìm đường đến ô đích.

***NORMAL (Màn 5–8)***

* Độ khó được tăng lên và bắt đầu xuất hiện nhiều cơ chế đặc biệt:

* Công tắc mở cầu.

* Ô gạch có thể bị vỡ.

* Nhiều hướng di chuyển khác nhau.

* Yêu cầu người chơi lựa chọn đường đi an toàn.

***HARD (Màn 9–12)***

* Các màn chơi nâng cao, kết hợp nhiều cơ chế của trò chơi.

***Đặc điểm:***

* Kết hợp nhiều loại cơ chế trong cùng một màn.

* Có ít đường đi an toàn.

* Yêu cầu lập kế hoạch nhiều bước.

* Người chơi cần tính toán chính xác trạng thái và vị trí của khối trước mỗi bước di chuyển.

# 3. Yêu cầu hệ thống

## 3.1. Phiên bản Python

Python 3.13.0

## 3.2. Thư viện

* Các thư viện cần thiết được liệt kê trong file: ***requirements.txt***

* Thư viện chính được sử dụng:

* ursina == 8.3.0

# 4. Cài đặt

***Để chạy chương trình, cần tải đầy đủ các tệp được cung cấp trong phần nộp bài của nhóm, bao gồm:***

- Các file Python (.py).

- Các file bản đồ (.json).

- Hình ảnh nền.

- Các tài nguyên cần thiết khác.

- File requirements.txt.

Sau khi tải về, giữ nguyên cấu trúc thư mục của dự án để chương trình có thể tìm thấy các file tài nguyên.

***Cài đặt các thư viện cần thiết bằng lệnh:***

```pip install -r requirements.txt```

# 5. Cách chạy chương trình

Mở Terminal hoặc Command Prompt tại thư mục gốc của dự án.

Chạy chương trình bằng lệnh:

```python main.py```

Sau khi chương trình được khởi động, giao diện chính của game sẽ xuất hiện.

Người chơi có thể lựa chọn:

- PLAY: Chơi game bằng cách điều khiển thủ công.

- SOLVER: Chọn thuật toán tìm kiếm để hỗ trợ giải màn chơi.

# 6. Cách chơi

## 6.1. Điều khiển khối

Người chơi có thể sử dụng một trong hai cách sau để di chuyển:

- Phím W, A, S, D.

- Các phím mũi tên (Arrow Keys).

Mỗi lần di chuyển sẽ làm thay đổi vị trí và trạng thái của khối.

= Mục tiêu của người chơi là đưa khối đến ô đích (Goal) và đặt khối ở trạng thái đứng để hoàn thành màn chơi.

## 6.2. Điều khiển khi khối bị tách

Ở một số màn chơi, người chơi có thể gặp công tắc khiến khối bị tách thành hai khối 1×1×1.

Khi khối đã bị tách, có thể sử dụng:

- Phím Tab

- Hoặc phím Space

để chuyển quyền điều khiển giữa hai khối.

Người chơi cần điều khiển hai khối một cách hợp lý để tiếp tục vượt qua màn chơi.

# 7. Chế độ Solver

Game cung cấp chế độ Solver nhằm hỗ trợ tìm đường giải cho các màn chơi.

Người chơi có thể lựa chọn các thuật toán tìm kiếm thuộc nhóm Uninformed Search để giải màn chơi.

Các thuật toán được hỗ trợ gồm:

- **BFS (Breadth-First Search):** Tìm kiếm theo chiều rộng.
- **DFS (Depth-First Search):** Tìm kiếm theo chiều sâu.
- **UCS (Uniform-Cost Search):** Tìm kiếm theo chi phí đồng nhất.
- **A\* (A-Star):** Thuật toán tìm kiếm có sử dụng hàm heuristic để định hướng quá trình tìm kiếm.

Ngoài ra, dự án có thể mở rộng với các thuật toán tìm kiếm khác tùy theo phạm vi triển khai của nhóm.