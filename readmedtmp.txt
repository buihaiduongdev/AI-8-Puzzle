# Giải Bài Toán 8-Puzzle Sử Dụng Thuật Toán Tìm Kiếm AI

## 1. Mục Tiêu

Dự án này nhằm mục đích triển khai và so sánh hiệu suất của các thuật toán tìm kiếm AI trong việc giải quyết bài toán 8-puzzle. Qua đó, người học có thể hiểu rõ hơn về cách hoạt động, ưu nhược điểm của từng thuật toán và ứng dụng chúng vào các bài toán thực tế.

---

## 2. Nội Dung

### 2.1 Các Thuật Toán Tìm Kiếm Không Thông Tin (Uninformed Search)

#### Danh sách thuật toán:
1. **BFS (Breadth-First Search):** Tìm kiếm theo chiều rộng, đảm bảo tìm được đường đi ngắn nhất.
   ![BFS Animation](https://raw.githubusercontent.com/buihaiduongdev/project-images/main/AI-Personal-Project/bfs-ezgif.com-video-to-gif-converter.gif)
2. **DFS (Depth-First Search):** Tìm kiếm theo chiều sâu, ưu tiên đi sâu trước.
   ![DFS Animation](https://raw.githubusercontent.com/buihaiduongdev/project-images/main/AI-Personal-Project/dfs-ezgif.com-video-to-gif-converter.gif)
3. **IDDFS (Iterative Deepening Depth-First Search):** Tìm kiếm sâu dần lặp, kết hợp ưu điểm của BFS và DFS.
   ![IDDFS Animation](https://raw.githubusercontent.com/buihaiduongdev/project-images/main/AI-Personal-Project/idf-ezgif.com-video-to-gif-converter.gif)
4. **UCS (Uniform Cost Search):** Tìm kiếm chi phí thống nhất, mở rộng nút có chi phí thấp nhất.
   ![UCS Animation](https://raw.githubusercontent.com/buihaiduongdev/project-images/main/AI-Personal-Project/ucs-ezgif.com-video-to-gif-converter.gif)

---

### 2.2 Các Thuật Toán Tìm Kiếm Có Thông Tin (Informed Search)

#### Danh sách thuật toán:
1. **A\* (A-Star):** Kết hợp chi phí đã đi (g) và chi phí ước lượng tới đích (h).
   ![A* Animation](https://raw.githubusercontent.com/buihaiduongdev/project-images/main/AI-Personal-Project/as-ezgif.com-video-to-gif-converter.gif)
2. **IDA\* (Iterative Deepening A-Star):** Phiên bản A\* tiết kiệm bộ nhớ hơn.
   ![IDA* Animation](https://raw.githubusercontent.com/buihaiduongdev/project-images/main/AI-Personal-Project/idas-ezgif.com-video-to-gif-converter.gif)
3. **Greedy Best-First Search:** Tìm kiếm tham lam, chọn bước đi có vẻ gần đích nhất.
   ![Greedy Animation](https://raw.githubusercontent.com/buihaiduongdev/project-images/main/AI-Personal-Project/gd-ezgif.com-video-to-gif-converter.gif)
4. **Local Beam Search:** Tìm kiếm chùm tia cục bộ, mở rộng nhiều trạng thái cùng lúc.
   *(GIF chưa có)*

---

### 2.3 Các Thuật Toán Tìm Kiếm Cục Bộ (Local Search)

#### Danh sách thuật toán:
1. **Simple Hill Climbing (HC):** Leo đồi đơn giản, chọn bước đi đầu tiên tốt hơn.
   ![Simple HC Animation](https://raw.githubusercontent.com/buihaiduongdev/project-images/main/AI-Personal-Project/shc-ezgif.com-video-to-gif-converter.gif)
2. **Steepest Ascent Hill Climbing (HC):** Leo đồi dốc nhất, chọn bước đi tốt nhất.
   ![Steepest HC Animation](https://raw.githubusercontent.com/buihaiduongdev/project-images/main/AI-Personal-Project/sthc-ezgif.com-video-to-gif-converter.gif)
3. **Stochastic Hill Climbing (HC):** Leo đồi ngẫu nhiên, chọn ngẫu nhiên bước đi tốt hơn.
   ![Stochastic HC Animation](https://raw.githubusercontent.com/buihaiduongdev/project-images/main/AI-Personal-Project/stohc-ezgif.com-video-to-gif-converter.gif)
4. **Simulated Annealing (SA):** Luyện thép mô phỏng, cho phép di chuyển đến trạng thái xấu hơn với xác suất giảm dần.
   ![Simulated Annealing Animation](https://raw.githubusercontent.com/buihaiduongdev/project-images/main/AI-Personal-Project/sa-ezgif.com-video-to-gif-converter.gif)
5. **Genetic Algorithm (GA):** Thuật toán di truyền, tiến hóa qua các thế hệ để tìm lời giải.
   ![Genetic Algorithm Animation](https://raw.githubusercontent.com/buihaiduongdev/project-images/main/AI-Personal-Project/ga-ezgif.com-video-to-gif-converter.gif)

---

### 2.4 Các Thuật Toán Khác

#### Danh sách thuật toán:
1. **Sensorless Search:** Tìm kiếm không cảm biến, áp dụng cho các trạng thái không xác định.
   ![BFS Sensorless Animation](https://raw.githubusercontent.com/buihaiduongdev/project-images/main/AI-Personal-Project/sl-ezgif.com-video-to-gif-converter.gif)
2. **Backtracking (BT):** Quay lui, duyệt sâu và quay lại khi gặp ngõ cụt.
   ![Backtracking Animation](https://raw.githubusercontent.com/buihaiduongdev/project-images/main/AI-Personal-Project/bt-ezgif.com-video-to-gif-converter.gif)
3. **CSP Backtracking (CSP BT):** Quay lui CSP, áp dụng cho bài toán thỏa mãn ràng buộc.
   ![CSP Backtracking Animation](https://raw.githubusercontent.com/buihaiduongdev/project-images/main/AI-Personal-Project/csp-ezgif.com-video-to-gif-converter.gif)
4. **Q-Learning (QL):** Học tăng cường, học chính sách tối ưu thông qua thử và sai.
   ![Q-Learning Animation](https://raw.githubusercontent.com/buihaiduongdev/project-images/main/AI-Personal-Project/ql-ezgif.com-video-to-gif-converter.gif)

---

## 3. So Sánh Hiệu Suất Các Thuật Toán

| Thuật Toán         | Đảm Bảo Tối Ưu | Bộ Nhớ Sử Dụng | Tốc Độ Thực Thi | Ghi Chú                          |
|---------------------|----------------|-----------------|-----------------|----------------------------------|
| BFS                | Có             | Cao             | Chậm            | Tìm đường đi ngắn nhất.          |
| DFS                | Không          | Thấp            | Nhanh           | Có thể rơi vào vòng lặp vô hạn. |
| IDDFS              | Có             | Trung bình      | Chậm hơn DFS    | Kết hợp ưu điểm của BFS và DFS. |
| UCS                | Có             | Cao             | Chậm            | Tương tự BFS khi chi phí là 1.  |
| A*                 | Có             | Trung bình      | Nhanh           | Hiệu quả với heuristic tốt.     |
| IDA*               | Có             | Thấp            | Chậm hơn A*     | Tiết kiệm bộ nhớ hơn A*.        |
| Greedy             | Không          | Trung bình      | Nhanh           | Không đảm bảo tối ưu.           |
| Local Beam Search  | Không          | Cao             | Trung bình      | Hiệu quả với không gian lớn.    |
| Hill Climbing      | Không          | Thấp            | Nhanh           | Dễ bị kẹt ở cực tiểu địa phương.|
| Simulated Annealing| Không          | Thấp            | Trung bình      | Có thể thoát khỏi cực tiểu.     |
| Genetic Algorithm  | Không          | Cao             | Chậm            | Phụ thuộc vào tham số tiến hóa. |
| Sensorless Search  | Không          | Cao             | Chậm            | Áp dụng cho trạng thái không xác định. |
| Backtracking       | Không          | Thấp            | Chậm            | Hiệu quả với không gian nhỏ.    |
| CSP Backtracking   | Không          | Trung bình      | Chậm            | Áp dụng cho bài toán CSP.       |
| Q-Learning         | Không          | Cao             | Rất chậm        | Cần thời gian huấn luyện dài.   |

---

## 4. Kết Luận

Dự án này cung cấp một cái nhìn tổng quan về các thuật toán tìm kiếm AI, từ các thuật toán cơ bản đến nâng cao. Việc triển khai và so sánh hiệu suất giúp người học hiểu rõ hơn về cách lựa chọn thuật toán phù hợp cho từng bài toán cụ thể.
------Yêu cầu---------
Các nhóm thuật toán:
uninformed search
	bfs
	dfs
	iterdive deeping
	UCS
informed search
	A*
	IDA*
	Greedy
	local beam
local search
	HC
	HC
	HC
	SA
	GA
complex environments
	sensorless
csps
	BT
	csp bt
Reinforecement learning
	QL

---templates----
1. mục tiêu
2. nội dung
2.1 các thuật toán tìm kiếm không thông tin
	trình bày các phần chính của bài toán tìm kiếm? sulotion là gì
	ảnh gif thuật toán
	nhận xét về hiệu suất của thuật toán khi áp dụng bài dự án AI-8-puzzle
2.2 ...
2.3...

so sánh hiệu xuất các thuật toán