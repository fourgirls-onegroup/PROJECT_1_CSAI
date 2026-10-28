# 1. Giới thiệu dự án

## Tên dự án: Bloxorz

Bloxorz là trò chơi giải đố trong đó người chơi điều khiển một khối hình chữ nhật trên một hệ thống các ô gạch để đưa khối đến vị trí đích. Người chơi cần tính toán hướng di chuyển và trạng thái của khối để vượt qua từng màn chơi.

Trò chơi được xây dựng bằng Python và thư viện Ursina Engine, đồng thời tích hợp các thuật toán tìm kiếm để hỗ trợ giải màn chơi.

# 2. Phân loại màn chơi

Các màn chơi được chia thành 3 mức độ:

### EASY (Màn 1–4)

Các màn chơi cơ bản, giúp người chơi làm quen với những cơ chế chính của trò chơi:

* Cách điều khiển và di chuyển khối.
* Các trạng thái của khối.
* Luật di chuyển và điều kiện hợp lệ.
* Cách sử dụng các công tắc để mở cầu.
* Cơ chế ô gạch có thể bị vỡ.
* Cách xác định và tìm đường đến ô đích.

### NORMAL (Màn 5–8)

Độ khó được nâng lên với sự kết hợp của nhiều cơ chế và yêu cầu người chơi đưa ra lựa chọn hợp lý:

* Công tắc điều khiển cầu.
* Ô gạch có thể bị vỡ.
* Nhiều hướng di chuyển và lựa chọn đường đi.
* Yêu cầu người chơi cân nhắc và lựa chọn tuyến đường an toàn.

### DIFFICULT (Màn 9–12)

Các màn chơi nâng cao, yêu cầu người chơi vận dụng và kết hợp nhiều cơ chế của trò chơi để hoàn thành màn chơi.

**Đặc điểm:**

* Kết hợp nhiều loại cơ chế trong cùng một màn chơi.
* Số lượng đường đi an toàn bị hạn chế.
* Yêu cầu lập kế hoạch và dự đoán nhiều bước di chuyển.
* Người chơi phải tính toán chính xác trạng thái và vị trí của khối trước mỗi bước đi.

# 3. Yêu cầu hệ thống

## 3.1. Phiên bản Python

Python 3.13.0

## 3.2. Thư viện

- Các thư viện cần thiết được liệt kê trong file **requirements.txt**.
- Thư viện chính được sử dụng:
  - **Ursina == 8.3.0**

# 4. Cài đặt

***Để chạy chương trình, cần tải đầy đủ các tệp được cung cấp trong phần nộp bài của nhóm, bao gồm:***

- Các file Python (.py).

- Các file bản đồ (.json).

- Tài nguyên hình ảnh và font chữ: Bao gồm file hình ảnh nền `.jpg` và các file font chữ `.ttf` được sử dụng trong trò chơi.

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

- Mục tiêu của người chơi là đưa khối đến ô đích (Goal) và đặt khối ở trạng thái đứng để hoàn thành màn chơi.

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