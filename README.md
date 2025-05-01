# Giải Bài Toán 8-Puzzle Sử Dụng Thuật Toán Tìm Kiếm AI (Đồ án môn Trí Tuệ Nhân Tạo)

## Mục Lục

*   [Giới thiệu](#giới-thiệu)
*   [Các Thuật Toán Được Triển Khai](#các-thuật-toán-được-triển-khai)
*   [Công Nghệ Sử Dụng](#công-nghệ-sử-dụng)
*   [Cài Đặt](#cài-đặt)
*   [Cách Sử Dụng](#cách-sử-dụng)
*   [Minh Họa Hoạt Động](#minh-họa-hoạt-động)
*   [Các Hạn Chế và Hướng Phát Triển](#các-hạn-chế-và-hướng-phát-triển)

## Giới thiệu

Dự án này là một phần của đồ án môn học Trí tuệ nhân tạo, tập trung vào việc áp dụng các thuật toán tìm kiếm AI để giải quyết bài toán 8-puzzle. Bài toán yêu cầu sắp xếp lại các ô số trên một bảng 3x3 từ một trạng thái ban đầu cho trước để đạt được trạng thái đích mong muốn, thông qua việc di chuyển ô trống.

Giao diện đồ họa được xây dựng bằng thư viện Pygame, cho phép người dùng chọn thuật toán, bắt đầu quá trình giải, quan sát các bước di chuyển (animation) và xem kết quả đường đi cũng như thời gian thực thi.

## Các Thuật Toán Được Triển Khai

Chương trình hiện thực hóa một loạt các thuật toán tìm kiếm và học máy, bao gồm:

1.  **Tìm kiếm không thông tin (Uninformed Search):**
    *   Tìm kiếm theo chiều rộng (BFS - Breadth-First Search): Đảm bảo tìm ra đường đi ngắn nhất về số bước.
    *   Tìm kiếm theo chiều sâu (DFS - Depth-First Search): Ưu tiên đi sâu, có thể không tối ưu, giới hạn độ sâu để tránh vòng lặp vô hạn.
    *   Tìm kiếm chi phí thống nhất (UCS - Uniform Cost Search): Mở rộng nút có chi phí đường đi thấp nhất từ gốc. Tương tự BFS khi chi phí mỗi bước là 1.
    *   Tìm kiếm sâu dần lặp (IDDFS - Iterative Deepening Depth-First Search): Kết hợp ưu điểm của DFS (bộ nhớ) và BFS (tối ưu số bước).

2.  **Tìm kiếm có thông tin (Informed Search):** (Sử dụng Heuristic Khoảng cách Manhattan)
    *   Tìm kiếm Tham lam Tốt nhất đầu tiên (Greedy Best-First Search): Chọn bước đi có vẻ gần đích nhất dựa trên heuristic, không đảm bảo tối ưu.
    *   A* (A-Star): Kết hợp chi phí đã đi (g) và chi phí ước lượng tới đích (h), đảm bảo tìm đường đi tối ưu nếu heuristic chấp nhận được.
    *   IDA* (Iterative Deepening A-Star): Phiên bản A* tiết kiệm bộ nhớ hơn, sử dụng ngưỡng chi phí tăng dần.

3.  **Tìm kiếm cục bộ (Local Search):**
    *   Leo đồi đơn giản (Simple Hill Climbing): Chọn bước đi đầu tiên tốt hơn trạng thái hiện tại.
    *   Leo đồi dốc nhất (Steepest Ascent Hill Climbing): Chọn bước đi tốt nhất trong số các hàng xóm.
    *   Leo đồi ngẫu nhiên (Stochastic Hill Climbing): Chọn ngẫu nhiên một trong số các bước đi tốt hơn.
    *   Luyện thép mô phỏng (Simulated Annealing): Cho phép di chuyển đến trạng thái xấu hơn với xác suất giảm dần để thoát khỏi cực tiểu địa phương.

4.  **Thuật toán dựa trên quần thể / Tiến hóa:**
    *   Thuật toán Di truyền (Genetic Algorithm): Duy trì một quần thể các trạng thái, tiến hóa qua các thế hệ. *Sau khi tìm được trạng thái đích, chương trình sử dụng A* để tìm đường đi cụ thể.*

5.  **Các phương pháp khác:**
    *   Quay lui (Backtracking): Tương tự DFS, sử dụng stack để duyệt.
    *   Quay lui CSP (CSP Backtracking): Áp dụng tư duy của bài toán thỏa mãn ràng buộc, về cơ bản giống Backtracking trong ngữ cảnh này.
    *   Học tăng cường (Q-Learning): Học một chính sách (policy) thông qua thử và sai với phần thưởng/phạt để tìm đường đi.
    *   Tìm kiếm không cảm biến (BFS Sensorless): Tìm một chuỗi hành động hoạt động cho tất cả các trạng thái có thể có trong tập hợp trạng thái ban đầu (belief state).

## Công Nghệ Sử Dụng

*   **Ngôn ngữ lập trình:** Python 3.x
*   **Thư viện chính:**
    *   `Pygame`: Dùng để tạo giao diện người dùng đồ họa (GUI), vẽ bảng puzzle, hiển thị thông tin, xử lý sự kiện chuột và tạo animation.
*   **Thư viện chuẩn Python:**
    *   `time` (đặc biệt là `time.perf_counter` để đo thời gian chính xác)
    *   `heapq` (cho hàng đợi ưu tiên trong UCS, Greedy, A*)
    *   `collections.deque` (cho hàng đợi trong BFS, stack trong DFS/Backtracking)
    *   `collections.defaultdict` (cho Q-table trong Q-Learning)
    *   `random` (cho các thuật toán ngẫu nhiên như Hill Climbing, SA, GA, QL)
    *   `math` (cho hàm `exp` trong SA)
    *   `sys` (để thoát chương trình)

## Cài Đặt

1.  **Yêu cầu hệ thống:**
    *   Python 3 (phiên bản 3.7 trở lên được khuyến nghị).
    *   `pip` (trình quản lý gói của Python, thường đi kèm với Python).

2.  **Cài đặt thư viện Pygame:**
    Mở Terminal (Linux/macOS) hoặc Command Prompt/PowerShell (Windows) và chạy lệnh:
    ```bash
    pip install pygame
    ```

3.  **Tải mã nguồn:**
    Sao chép (clone) hoặc tải về mã nguồn của dự án này về máy tính của bạn.

## Cách Sử Dụng

1.  **Khởi chạy ứng dụng:**
    *   Mở Terminal/Command Prompt.
    *   Sử dụng lệnh `cd` để điều hướng đến thư mục bạn đã lưu mã nguồn.
    *   Chạy file Python chính bằng lệnh:
        ```bash
        python your_main_script_name.py
        ```
        *(Thay `your_main_script_name.py` bằng tên file thực tế, ví dụ: `main.py`)*

2.  **Tương tác với giao diện:**
    *   **Quan sát:** Giao diện chính hiển thị bảng 8-puzzle ở bên trái và khu vực điều khiển/thông tin ở bên phải.
    *   **Chọn thuật toán:** Nhấp vào hộp màu xanh lá có chữ "Select Algorithm" hoặc tên thuật toán đã chọn trước đó. Một danh sách các thuật toán sẽ hiện ra. Nhấp vào tên thuật toán bạn muốn sử dụng. Tên thuật toán sẽ được cập nhật trên hộp.
    *   **Bắt đầu giải:** Sau khi đã chọn thuật toán, nhấp vào nút "Start" màu xanh dương.
    *   **Theo dõi:** Chương trình sẽ bắt đầu chạy thuật toán. Thông tin về thời gian xử lý sẽ được cập nhật. Nếu thuật toán tìm được lời giải, animation các bước di chuyển sẽ được hiển thị trên bảng puzzle.
    *   **Xem kết quả:** Sau khi animation kết thúc (hoặc nếu thuật toán không tìm được lời giải/lỗi), đường đi (chuỗi 'U', 'D', 'L', 'R') hoặc thông báo kết quả sẽ hiển thị trong khu vực "Path:" ở phía dưới. Thời gian xử lý và thời gian hiển thị animation cuối cùng cũng được cập nhật.

## Minh Họa Hoạt Động

Các ảnh GIF dưới đây minh họa quá trình giải bài toán từ trạng thái bắt đầu `(2, 6, 5, 1, 3, 8, 4, 7, 0)` đến trạng thái đích `(1, 2, 3, 4, 5, 6, 7, 8, 0)` bằng các thuật toán khác nhau. Lưu ý rằng một số thuật toán (như các biến thể Hill Climbing hoặc Greedy) có thể không tìm ra đường đi tối ưu hoặc có thể bị kẹt.

**1. Tìm kiếm theo chiều rộng (BFS)**
*Đảm bảo đường đi ngắn nhất về số bước.*
![BFS Animation](https://raw.githubusercontent.com/buihaiduongdev/project-images/main/AI-Personal-Project/bfs-ezgif.com-video-to-gif-converter.gif)

**2. Tìm kiếm theo chiều sâu (DFS)**
*Ưu tiên đi sâu, đường đi thường không tối ưu, có giới hạn độ sâu.*
![DFS Animation](https://raw.githubusercontent.com/buihaiduongdev/project-images/main/AI-Personal-Project/dfs-ezgif.com-video-to-gif-converter.gif)

**3. Tìm kiếm sâu dần lặp (IDDFS)**
*Kết hợp ưu điểm bộ nhớ của DFS và tính tối ưu số bước của BFS.*
![IDDFS Animation](https://raw.githubusercontent.com/buihaiduongdev/project-images/main/AI-Personal-Project/idf-ezgif.com-video-to-gif-converter.gif)

**4. Tìm kiếm Tham lam (Greedy)**
*Nhanh chóng hướng về đích dựa trên heuristic, đường đi thường không tối ưu.*
![Greedy Animation](https://raw.githubusercontent.com/buihaiduongdev/project-images/main/AI-Personal-Project/gd-ezgif.com-video-to-gif-converter.gif)

**5. Tìm kiếm chi phí thống nhất (UCS)**
*Tìm đường đi có tổng chi phí (số bước) thấp nhất, tương tự BFS trong trường hợp này.*
![UCS Animation](https://raw.githubusercontent.com/buihaiduongdev/project-images/main/AI-Personal-Project/ucs-ezgif.com-video-to-gif-converter.gif)

**6. A* (A-Star)**
*Tìm đường đi tối ưu hiệu quả nhờ kết hợp chi phí thực tế và heuristic.*
![A* Animation](https://raw.githubusercontent.com/buihaiduongdev/project-images/main/AI-Personal-Project/as-ezgif.com-video-to-gif-converter.gif)

**7. IDA* (Iterative Deepening A*)**
*Phiên bản A* tiết kiệm bộ nhớ hơn.*
![IDA* Animation](https://raw.githubusercontent.com/buihaiduongdev/project-images/main/AI-Personal-Project/idas-ezgif.com-video-to-gif-converter.gif)

**8. Leo đồi đơn giản (Simple Hill Climbing)**
*Di chuyển đến hàng xóm tốt hơn đầu tiên tìm thấy, dễ bị kẹt.*
![Simple HC Animation](https://raw.githubusercontent.com/buihaiduongdev/project-images/main/AI-Personal-Project/sl-ezgif.com-video-to-gif-converter.gif)

**9. Leo đồi dốc nhất (Steepest Hill Climbing)**
*Di chuyển đến hàng xóm tốt nhất, vẫn có thể bị kẹt.*
![Steepest HC Animation](https://raw.githubusercontent.com/buihaiduongdev/project-images/main/AI-Personal-Project/sthc-ezgif.com-video-to-gif-converter.gif)

**10. Leo đồi ngẫu nhiên (Stochastic Hill Climbing)**
*Chọn ngẫu nhiên từ các hàng xóm tốt hơn.*
![Stochastic HC Animation](https://raw.githubusercontent.com/buihaiduongdev/project-images/main/AI-Personal-Project/stohc-ezgif.com-video-to-gif-converter.gif)

**11. Luyện thép mô phỏng (Simulated Annealing)**
*Có khả năng thoát khỏi cực tiểu địa phương bằng cách chấp nhận nước đi xấu hơn.*
![Simulated Annealing Animation](https://raw.githubusercontent.com/buihaiduongdev/project-images/main/AI-Personal-Project/sa-ezgif.com-video-to-gif-converter.gif)

**12. Thuật toán Di truyền (Genetic Algorithm)**
*Tìm trạng thái đích thông qua tiến hóa, sau đó dùng A* tìm đường đi.*
![Genetic Algorithm Animation](https://raw.githubusercontent.com/buihaiduongdev/project-images/main/AI-Personal-Project/ga-ezgif.com-video-to-gif-converter.gif)

**13. Quay lui (Backtracking)**
*Tương tự DFS, duyệt sâu và quay lại khi gặp ngõ cụt.*
![Backtracking Animation](https://raw.githubusercontent.com/buihaiduongdev/project-images/main/AI-Personal-Project/bt-ezgif.com-video-to-gif-converter.gif)

**14. Quay lui CSP (CSP Backtracking)**
*Áp dụng kỹ thuật quay lui trong ngữ cảnh bài toán thỏa mãn ràng buộc.*
![CSP Backtracking Animation](https://raw.githubusercontent.com/buihaiduongdev/project-images/main/AI-Personal-Project/csp-ezgif.com-video-to-gif-converter.gif)

**15. Học tăng cường (Q-Learning)**
*Học chính sách tối ưu qua nhiều lượt thử và sai (quá trình huấn luyện không hiển thị).*
![Q-Learning Animation](https://raw.githubusercontent.com/buihaiduongdev/project-images/main/AI-Personal-Project/ql-ezgif.com-video-to-gif-converter.gif)

*(Lưu ý: Không có ảnh GIF minh họa riêng cho BFS Sensorless)*
## Các Hạn Chế và Hướng Phát Triển

*   **Heuristic:** Hiện tại chỉ sử dụng heuristic khoảng cách Manhattan. Có thể thử nghiệm các heuristic khác (ví dụ: số ô sai vị trí - Misplaced Tiles) hoặc kết hợp heuristic.
*   **Genetic Algorithm:** Việc kết hợp GA với A* để tìm đường đi là một giải pháp phổ biến, nhưng có thể khám phá các cách khác để GA tự lưu trữ hoặc tái tạo lại đường đi. Hiệu quả của GA cũng phụ thuộc nhiều vào việc tinh chỉnh các tham số (kích thước quần thể, tỉ lệ đột biến, lai ghép,...).
*   **Q-Learning:** Hiệu suất phụ thuộc lớn vào việc thiết kế hàm thưởng và các siêu tham số (learning rate, discount factor, exploration rate). Thời gian huấn luyện có thể khá lâu.
*   **Giao diện người dùng:**
    *   Có thể cho phép người dùng nhập trạng thái bắt đầu và đích tùy chỉnh.
    *   Thêm chức năng tạm dừng/tiếp tục animation.
    *   Cải thiện cách hiển thị đường đi rất dài (ví dụ: thêm thanh cuộn cho khu vực Path).
    *   Trực quan hóa các nút đã được khám phá hoặc biên giới tìm kiếm.
*   **So sánh thuật toán:** Thêm tính năng chạy nhiều thuật toán và so sánh trực tiếp thời gian, số bước, số nút đã duyệt.
