# Giải Bài Toán 8-Puzzle Sử Dụng Thuật Toán Tìm Kiếm AI

## 1. Mục Tiêu

Dự án này nhằm mục đích triển khai, minh họa và so sánh hiệu suất của một loạt các thuật toán tìm kiếm và học máy thuộc lĩnh vực Trí tuệ Nhân tạo (AI) trong việc giải quyết bài toán 8-puzzle kinh điển. Mục tiêu là cung cấp một cái nhìn trực quan và thực tế về cách các thuật toán khác nhau tiếp cận bài toán, đồng thời làm nổi bật ưu và nhược điểm của chúng về tính tối ưu, thời gian thực thi và yêu cầu bộ nhớ. Qua đó, người học có thể hiểu sâu hơn về các nguyên tắc cơ bản của tìm kiếm trong AI.

---

## 2. Nội Dung
**Các thành phần chính của bài toán tìm kiếm 8-Puzzle được định nghĩa như sau:**
*   **Trạng thái (State):** Một cấu hình cụ thể của bảng 3x3.
*   **Trạng thái ban đầu (Initial State):** Cấu hình bảng lúc bắt đầu (`(2, 6, 5, 1, 3, 8, 4, 7, 0)`).
*   **Hành động (Actions):** Các hành động có thể thực hiện từ một trạng thái `s`, `ACTIONS(s)`, là di chuyển ô trống ('0') lên (Up - 'U'), xuống (Down - 'D'), trái (Left - 'L'), hoặc phải (Right - 'R') vào vị trí của ô kề cận (nếu hợp lệ).
*   **Hàm chuyển đổi (Transition Model):** Mô tả trạng thái kết quả `RESULT(s, a)` sau khi thực hiện một hành động `a` từ trạng thái `s`.
*   **Kiểm tra đích (Goal Test):** Kiểm tra xem trạng thái hiện tại có khớp với trạng thái đích mong muốn `GOAL = (1, 2, 3, 4, 5, 6, 7, 8, 0)` hay không.
*   **Chi phí đường đi (Path Cost):** Tổng chi phí của các bước đi từ trạng thái ban đầu đến trạng thái hiện tại, mỗi bước di chuyển có chi phí là 1.
*   **Lời giải (Solution):** Một chuỗi các hành động (ví dụ: 'DRUL...') dẫn từ trạng thái ban đầu đến trạng thái đích. Một lời giải tối ưu là lời giải có chi phí đường đi thấp nhất.
### 2.1. Các Thuật Toán Tìm Kiếm Không Thông Tin (Uninformed Search)

Các thuật toán này duyệt không gian trạng thái mà không sử dụng bất kỳ thông tin nào về đích đến. Chúng chỉ phân biệt được trạng thái đích và trạng thái không phải đích.

---

#### 1. Tìm kiếm theo chiều rộng (BFS - Breadth-First Search)
*   **Mô tả:** Mở rộng nút nông nhất chưa được mở rộng. Nó duyệt tất cả các nút ở độ sâu `k` trước khi duyệt bất kỳ nút nào ở độ sâu `k+1`. Sử dụng cấu trúc dữ liệu hàng đợi (Queue - First-In, First-Out).
*   **Minh họa:**
    ![BFS Animation](https://raw.githubusercontent.com/buihaiduongdev/project-images/main/AI-Personal-Project/bfs-ezgif.com-video-to-gif-converter.gif)
*   **Nhận xét về hiệu suất (8-Puzzle):**
    *   **Tính tối ưu:** Có. BFS đảm bảo tìm ra đường đi ngắn nhất (ít bước di chuyển nhất) vì nó luôn tìm thấy nút đích nông nhất trước.
    *   **Tính đầy đủ:** Có. Nếu có lời giải tồn tại, BFS chắc chắn sẽ tìm thấy nó.
    *   **Độ phức tạp thời gian:** O(b<sup>d</sup>), trong đó `b` là nhân tố nhánh (số hành động tối đa từ một trạng thái, tối đa là 4) và `d` là độ sâu của lời giải nông nhất. Có thể rất chậm nếu lời giải ở sâu.
    *   **Độ phức tạp không gian (bộ nhớ):** O(b<sup>d</sup>). BFS phải lưu trữ tất cả các nút ở biên giới tìm kiếm trong hàng đợi và các nút đã thăm. Đây là hạn chế lớn nhất của BFS, có thể nhanh chóng cạn kiệt bộ nhớ.

---

#### 2. Tìm kiếm theo chiều sâu (DFS - Depth-First Search)
*   **Mô tả:** Luôn mở rộng nút sâu nhất trong số các nút chưa được mở rộng ở biên giới tìm kiếm. Nó đi sâu vào một nhánh cho đến khi gặp nút lá hoặc đạt giới hạn độ sâu được đặt trước, sau đó mới quay lui và khám phá nhánh khác. Sử dụng cấu trúc dữ liệu ngăn xếp (Stack - Last-In, First-Out). Trong dự án này, một giới hạn độ sâu (`max_depth`) được áp dụng để tránh rơi vào các nhánh vô hạn hoặc quá dài.
*   **Minh họa:**
    ![DFS Animation](https://raw.githubusercontent.com/buihaiduongdev/project-images/main/AI-Personal-Project/dfs-ezgif.com-video-to-gif-converter.gif)
*   **Nhận xét về hiệu suất (8-Puzzle):**
    *   **Tính tối ưu:** Không. DFS không đảm bảo tìm ra đường đi ngắn nhất. Nó có thể tìm thấy một lời giải rất dài trước khi tìm thấy lời giải ngắn hơn (nếu có) ở nhánh khác.
    *   **Tính đầy đủ:** Không (nếu không gian trạng thái vô hạn hoặc có chu trình). Với giới hạn độ sâu `m`, nó chỉ đầy đủ nếu lời giải nông nhất có độ sâu `d <= m`. Nếu không giới hạn độ sâu và không kiểm tra trạng thái đã thăm, nó có thể bị kẹt trong vòng lặp.
    *   **Độ phức tạp thời gian:** O(b<sup>m</sup>), với `m` là độ sâu tối đa của không gian trạng thái (hoặc giới hạn độ sâu). Có thể nhanh hơn BFS nếu may mắn tìm thấy lời giải sớm, nhưng cũng có thể chậm hơn nhiều nếu lời giải nằm ở nhánh khác hoặc `m` lớn hơn `d` rất nhiều.
    *   **Độ phức tạp không gian (bộ nhớ):** O(b*m). Yêu cầu bộ nhớ thấp hơn nhiều so với BFS, chỉ cần lưu trữ đường đi hiện tại và các nút chưa khám phá dọc theo đường đi đó. Đây là ưu điểm chính của DFS.

---

#### 3. Tìm kiếm sâu dần lặp (IDDFS - Iterative Deepening Depth-First Search)
*   **Mô tả:** Kết hợp ưu điểm của BFS (tính tối ưu, đầy đủ) và DFS (yêu cầu bộ nhớ thấp). IDDFS thực hiện tìm kiếm giới hạn độ sâu (Depth-Limited Search - DLS) lặp đi lặp lại với giới hạn độ sâu tăng dần: 0, 1, 2, ..., cho đến khi tìm thấy lời giải.
*   **Minh họa:**
    ![IDDFS Animation](https://raw.githubusercontent.com/buihaiduongdev/project-images/main/AI-Personal-Project/idf-ezgif.com-video-to-gif-converter.gif)
*   **Nhận xét về hiệu suất (8-Puzzle):**
    *   **Tính tối ưu:** Có. Giống như BFS, nó sẽ tìm thấy lời giải nông nhất đầu tiên.
    *   **Tính đầy đủ:** Có. Giống như BFS.
    *   **Độ phức tạp thời gian:** O(b<sup>d</sup>). Mặc dù có vẻ lãng phí khi duyệt lại các nút ở tầng trên nhiều lần, nhưng số nút ở tầng cuối (tầng `d`) thường chiếm phần lớn tổng số nút, nên chi phí duyệt lại không quá đáng kể so với BFS.
    *   **Độ phức tạp không gian (bộ nhớ):** O(b*d). Giống như DFS, yêu cầu bộ nhớ thấp. IDDFS thường là thuật toán tìm kiếm không thông tin được ưa chuộng khi không gian tìm kiếm lớn và độ sâu lời giải không xác định.

---

#### 4. Tìm kiếm chi phí thống nhất (UCS - Uniform Cost Search)
*   **Mô tả:** Mở rộng nút `n` có chi phí đường đi `g(n)` (chi phí từ nút gốc đến `n`) thấp nhất trong số các nút chưa được mở rộng. Sử dụng hàng đợi ưu tiên (Priority Queue) để quản lý các nút ở biên giới, sắp xếp theo `g(n)`.
*   **Minh họa:**
    ![UCS Animation](https://raw.githubusercontent.com/buihaiduongdev/project-images/main/AI-Personal-Project/ucs-ezgif.com-video-to-gif-converter.gif)
*   **Nhận xét về hiệu suất (8-Puzzle):**
    *   **Tính tối ưu:** Có. UCS đảm bảo tìm ra đường đi có tổng chi phí thấp nhất. Khi chi phí mỗi bước là như nhau và dương (ví dụ, bằng 1 như trong 8-puzzle), UCS hoạt động giống hệt BFS và tìm ra đường đi ngắn nhất.
    *   **Tính đầy đủ:** Có (miễn là chi phí mỗi bước lớn hơn một hằng số dương nhỏ ε).
    *   **Độ phức tạp thời gian:** O(b<sup>1 + floor(C*/ε)</sup>), trong đó C* là chi phí của lời giải tối ưu. Khi chi phí bước là 1 (ε=1) và C*=d, độ phức tạp trở thành O(b<sup>d+1</sup>) hoặc O(b<sup>d</sup>) tùy cách cài đặt, tương đương BFS.
    *   **Độ phức tạp không gian (bộ nhớ):** O(b<sup>1 + floor(C*/ε)</sup>). Tương tự BFS, UCS thường yêu cầu bộ nhớ rất lớn vì phải lưu trữ nhiều nút trong hàng đợi ưu tiên.

---

### 2.2. Các Thuật Toán Tìm Kiếm Có Thông Tin (Informed Search / Heuristic Search)

Các thuật toán này sử dụng một hàm heuristic `h(n)` để ước lượng chi phí từ trạng thái hiện tại `n` đến trạng thái đích. Heuristic này cung cấp "thông tin" về đích đến, giúp hướng dẫn tìm kiếm hiệu quả hơn so với tìm kiếm mù quáng. Trong dự án này, heuristic chính được sử dụng là **Khoảng cách Manhattan**: `h(n)` là tổng khoảng cách (tính theo số ô di chuyển ngang và dọc) mà mỗi ô số (từ 1 đến 8) phải di chuyển từ vị trí hiện tại của nó trong trạng thái `n` để về đúng vị trí trong trạng thái đích.

**Lời giải (Solution):** Vẫn là một chuỗi các hành động dẫn từ trạng thái ban đầu đến trạng thái đích, thường là lời giải tối ưu (chi phí thấp nhất) nếu thuật toán và heuristic phù hợp.

---

#### 1. A* (A-Star Search)
*   **Mô tả:** Kết hợp ưu điểm của UCS (ưu tiên đường đi chi phí thấp `g(n)`) và Greedy Best-First Search (ưu tiên trạng thái gần đích `h(n)`). A* mở rộng nút `n` có giá trị hàm đánh giá `f(n) = g(n) + h(n)` thấp nhất. Nó sử dụng hàng đợi ưu tiên sắp xếp theo `f(n)`.
*   **Minh họa:**
    ![A* Animation](https://raw.githubusercontent.com/buihaiduongdev/project-images/main/AI-Personal-Project/as-ezgif.com-video-to-gif-converter.gif)
*   **Nhận xét về hiệu suất (8-Puzzle):**
    *   **Tính tối ưu:** Có. A* đảm bảo tìm ra đường đi tối ưu nếu hàm heuristic `h(n)` là **chấp nhận được (admissible)**, nghĩa là `h(n)` không bao giờ đánh giá quá cao chi phí thực tế để đạt đích (luôn ≤ chi phí thực tế). Khoảng cách Manhattan là một heuristic chấp nhận được cho 8-puzzle. Tính tối ưu cũng đòi hỏi `h(n)` **nhất quán (consistent)** hoặc có kiểm tra trạng thái đã thăm khi một nút được tìm thấy lại qua đường đi tốt hơn.
    *   **Tính đầy đủ:** Có.
    *   **Độ phức tạp thời gian:** Phụ thuộc mạnh vào chất lượng của heuristic. Với heuristic tốt, A* có thể hiệu quả hơn nhiều so với các thuật toán không thông tin. Trong trường hợp xấu nhất, nó có thể suy biến thành BFS/UCS.
    *   **Độ phức tạp không gian (bộ nhớ):** Vẫn có thể rất lớn. A* lưu trữ tất cả các nút đã được sinh ra trong bộ nhớ (trong hàng đợi ưu tiên và danh sách đóng). Đây là hạn chế chính của A*.

---

#### 2. IDA* (Iterative Deepening A-Star)
*   **Mô tả:** Là phiên bản lặp sâu của A*, nhằm giảm yêu cầu bộ nhớ của A*. IDA* thực hiện một chuỗi các tìm kiếm theo chiều sâu. Trong mỗi lần lặp, nó sử dụng một ngưỡng cắt (cut-off) dựa trên giá trị `f(n) = g(n) + h(n)`. Nó chỉ duyệt các nút có `f(n)` không vượt quá ngưỡng hiện tại. Ngưỡng bắt đầu bằng `f(start_node)` và tăng lên giá trị `f` thấp nhất đã bị cắt ở lần lặp trước đó.
*   **Minh họa:**
    ![IDA* Animation](https://raw.githubusercontent.com/buihaiduongdev/project-images/main/AI-Personal-Project/idas-ezgif.com-video-to-gif-converter.gif)
*   **Nhận xét về hiệu suất (8-Puzzle):**
    *   **Tính tối ưu:** Có (với heuristic chấp nhận được, giống A*).
    *   **Tính đầy đủ:** Có.
    *   **Độ phức tạp thời gian:** Tương tự A* về mặt lý thuyết, nhưng có thể chậm hơn trong thực tế do phải duyệt lại các nút ở các lần lặp trước. Tuy nhiên, nếu số lượng nút tăng mạnh theo giá trị `f`, chi phí duyệt lại không quá lớn.
    *   **Độ phức tạp không gian (bộ nhớ):** O(b*d). Giống như IDDFS, IDA* chỉ yêu cầu bộ nhớ tuyến tính theo độ sâu của lời giải. Đây là ưu điểm vượt trội so với A* cho các bài toán có không gian trạng thái rất lớn.

---

#### 3. Tìm kiếm Tham lam Tốt nhất đầu tiên (Greedy Best-First Search)
*   **Mô tả:** Mở rộng nút `n` có vẻ "hứa hẹn" nhất, tức là nút được đánh giá là gần đích nhất theo hàm heuristic `h(n)`. Nó bỏ qua chi phí đã đi `g(n)` và chỉ cố gắng giảm thiểu `h(n)`. Sử dụng hàng đợi ưu tiên chỉ dựa trên `h(n)`.
*   **Minh họa:**
    ![Greedy Animation](https://raw.githubusercontent.com/buihaiduongdev/project-images/main/AI-Personal-Project/gd-ezgif.com-video-to-gif-converter.gif)
*   **Nhận xét về hiệu suất (8-Puzzle):**
    *   **Tính tối ưu:** Không. Vì bỏ qua `g(n)`, nó có thể đi vào một đường dài mặc dù có vẻ gần đích ở mỗi bước.
    *   **Tính đầy đủ:** Không. Có thể đi vào vòng lặp nếu không kiểm tra trạng thái đã thăm. Nó cũng có thể bị kẹt và không tìm thấy lời giải ngay cả khi nó tồn tại.
    *   **Độ phức tạp thời gian:** Thường nhanh hơn A* hoặc BFS để tìm ra *một* lời giải (không nhất thiết tối ưu), nhưng độ phức tạp trong trường hợp xấu nhất vẫn có thể là O(b<sup>m</sup>).
    *   **Độ phức tạp không gian (bộ nhớ):** Tương tự thời gian, thường ít hơn A* nhưng trong trường hợp xấu nhất cũng là O(b<sup>m</sup>).


### 2.3. Các Thuật Toán Tìm Kiếm Cục Bộ (Local Search)

Các thuật toán này hoạt động bằng cách duy trì và cải thiện một trạng thái hiện tại duy nhất (hoặc một tập nhỏ các trạng thái như trong GA), thay vì duyệt có hệ thống toàn bộ cây tìm kiếm. Chúng di chuyển từ trạng thái hiện tại đến các trạng thái lân cận, thường dựa trên một hàm mục tiêu (objective function) hoặc hàm đánh giá (heuristic `h(n)` trong trường hợp này, với mục tiêu là tối thiểu hóa `h(n)` về 0). Chúng thường không lưu trữ đường đi đã qua.

**Lời giải (Solution):** Mục tiêu chính là tìm được một trạng thái thỏa mãn điều kiện đích (`h(n)=0`). Bản thân thuật toán thường không cung cấp đường đi từ trạng thái ban đầu đến trạng thái đích đó. Nếu cần đường đi, phải có cơ chế bổ sung (ví dụ: ghi lại các bước di chuyển trong quá trình tìm kiếm, hoặc dùng thuật toán khác như A* để tìm đường đi sau khi đã biết trạng thái đích như trong triển khai GA của dự án này).

---

#### 1. Leo đồi đơn giản (Simple Hill Climbing - HC)
*   **Mô tả:** Bắt đầu từ trạng thái hiện tại, liên tục di chuyển đến một trạng thái lân cận tốt hơn (có giá trị heuristic `h(n)` thấp hơn). Nó chọn hành động *đầu tiên* dẫn đến trạng thái tốt hơn mà nó tìm thấy. Nếu không có trạng thái lân cận nào tốt hơn trạng thái hiện tại, thuật toán dừng lại.
*   **Minh họa:**
    ![Simple HC Animation](https://raw.githubusercontent.com/buihaiduongdev/project-images/main/AI-Personal-Project/shc-ezgif.com-video-to-gif-converter.gif)
*   **Nhận xét về hiệu suất (8-Puzzle):**
    *   **Tính tối ưu/Đầy đủ:** Không. Thuật toán rất dễ bị "mắc kẹt" tại:
        *   **Cực tiểu địa phương (Local Minimum):** Một trạng thái tốt hơn tất cả các hàng xóm của nó nhưng không phải là tốt nhất toàn cục (trạng thái đích).
        *   **Bình nguyên (Plateau):** Một vùng không gian trạng thái phẳng nơi các hàng xóm có cùng giá trị heuristic, khiến thuật toán không biết đi đâu.
        *   **Sườn núi (Ridge):** Một khu vực khó di chuyển lên theo hướng tối ưu.
    *   **Độ phức tạp thời gian:** Rất nhanh ở mỗi bước, vì chỉ cần tìm một hàng xóm tốt hơn. Tổng thời gian phụ thuộc vào việc có bị kẹt sớm hay không.
    *   **Độ phức tạp không gian (bộ nhớ):** O(1). Chỉ cần lưu trữ trạng thái hiện tại.

---

#### 2. Leo đồi dốc nhất (Steepest Ascent Hill Climbing - HC)
*   **Mô tả:** Tương tự Simple Hill Climbing, nhưng thay vì chọn hàng xóm tốt hơn đầu tiên, nó đánh giá *tất cả* các hàng xóm và chọn di chuyển đến hàng xóm *tốt nhất* (có giá trị `h(n)` thấp nhất). Nếu không có hàng xóm nào tốt hơn trạng thái hiện tại, thuật toán dừng lại.
*   **Minh họa:**
    ![Steepest HC Animation](https://raw.githubusercontent.com/buihaiduongdev/project-images/main/AI-Personal-Project/sthc-ezgif.com-video-to-gif-converter.gif)
*   **Nhận xét về hiệu suất (8-Puzzle):**
    *   **Tính tối ưu/Đầy đủ:** Không. Vẫn có thể bị kẹt ở cực tiểu địa phương, bình nguyên, sườn núi, mặc dù có thể đi xa hơn Simple HC trong một số trường hợp.
    *   **Độ phức tạp thời gian:** Chậm hơn Simple HC ở mỗi bước vì phải đánh giá tất cả các hàng xóm.
    *   **Độ phức tạp không gian (bộ nhớ):** O(1).

---

#### 3. Leo đồi ngẫu nhiên (Stochastic Hill Climbing - HC)
*   **Mô tả:** Chọn ngẫu nhiên một trong số các trạng thái lân cận tốt hơn trạng thái hiện tại. Xác suất chọn có thể đồng đều hoặc phụ thuộc vào mức độ cải thiện (hàng xóm càng tốt thì xác suất được chọn càng cao).
*   **Minh họa:**
    ![Stochastic HC Animation](https://raw.githubusercontent.com/buihaiduongdev/project-images/main/AI-Personal-Project/stohc-ezgif.com-video-to-gif-converter.gif)
*   **Nhận xét về hiệu suất (8-Puzzle):**
    *   **Tính tối ưu/Đầy đủ:** Không. Vẫn có thể bị kẹt, nhưng tính ngẫu nhiên có thể giúp khám phá các phần khác nhau của sườn dốc so với các phiên bản tất định.
    *   **Độ phức tạp thời gian:** Tốc độ thay đổi tùy thuộc vào việc chọn ngẫu nhiên, thường nhanh.
    *   **Độ phức tạp không gian (bộ nhớ):** O(1).

---

#### 4. Luyện thép mô phỏng (Simulated Annealing - SA)
*   **Mô tả:** Là một thuật toán leo đồi ngẫu nhiên có khả năng thoát khỏi cực tiểu địa phương. Nó cho phép di chuyển đến trạng thái *xấu hơn* (heuristic cao hơn) với một xác suất nhất định. Xác suất này (`P = exp(-ΔE/T)`) phụ thuộc vào mức độ xấu đi (`ΔE = h(next) - h(current) > 0`) và một tham số "nhiệt độ" (`T`). Ban đầu, `T` cao, cho phép di chuyển xấu nhiều hơn (khám phá rộng). Dần dần, `T` giảm theo một "lịch trình làm nguội" (cooling schedule), khiến xác suất chấp nhận nước đi xấu giảm xuống, thuật toán trở nên "tham lam" hơn (khai thác).
*   **Minh họa:**
    ![Simulated Annealing Animation](https://raw.githubusercontent.com/buihaiduongdev/project-images/main/AI-Personal-Project/sa-ezgif.com-video-to-gif-converter.gif)
*   **Nhận xét về hiệu suất (8-Puzzle):**
    *   **Tính tối ưu:** Không đảm bảo tối ưu toàn cục, nhưng có khả năng tìm được lời giải tốt hơn đáng kể so với các phiên bản Hill Climbing đơn giản do khả năng thoát khỏi cực tiểu địa phương.
    *   **Tính đầy đủ:** Nếu lịch trình làm nguội đủ chậm (T giảm từ từ), SA được chứng minh là sẽ hội tụ về trạng thái tối ưu toàn cục với xác suất tiến tới 1. Tuy nhiên, trong thực tế, lịch trình thường nhanh hơn để tiết kiệm thời gian.
    *   **Độ phức tạp thời gian:** Thường chậm hơn Hill Climbing do có thể khám phá nhiều trạng thái hơn và cần tính toán xác suất. Hiệu suất phụ thuộc nhiều vào lịch trình làm nguội.
    *   **Độ phức tạp không gian (bộ nhớ):** O(1).

---

#### 5. Thuật toán Di truyền (Genetic Algorithm - GA)
*   **Mô tả:** Là một thuật toán tìm kiếm dựa trên quần thể, mô phỏng quá trình chọn lọc tự nhiên và di truyền. Nó duy trì một tập hợp (quần thể - population) các trạng thái (cá thể - individuals). Ở mỗi thế hệ:
    *   Đánh giá độ thích nghi (fitness) của mỗi cá thể (thường dựa trên heuristic, ví dụ: fitness càng cao khi `h(n)` càng thấp).
    *   Chọn lọc (Selection): Các cá thể có độ thích nghi cao hơn có nhiều khả năng được chọn làm cha mẹ cho thế hệ sau.
    *   Lai ghép (Crossover): Kết hợp vật liệu di truyền (đặc điểm trạng thái) của hai cha mẹ để tạo ra con cái mới.
    *   Đột biến (Mutation): Thay đổi ngẫu nhiên một phần nhỏ trong cá thể con để duy trì sự đa dạng di truyền.
    Quá trình lặp lại qua nhiều thế hệ, hy vọng quần thể sẽ tiến hóa đến các giải pháp ngày càng tốt hơn.
    *Lưu ý quan trọng:* Trong triển khai của dự án này, GA được sử dụng để tìm ra một trạng thái *đích* (một cá thể có `h(n) = 0`). Sau khi GA tìm thấy trạng thái đích này, thuật toán **A\*** mới được gọi để tìm đường đi cụ thể từ trạng thái ban đầu đến trạng thái đích mà GA đã tìm ra. Bản thân GA không trực tiếp tìm đường đi.
*   **Minh họa (Hiển thị đường đi tìm bởi A* sau khi GA tìm được trạng thái đích):**
    ![Genetic Algorithm Animation](https://raw.githubusercontent.com/buihaiduongdev/project-images/main/AI-Personal-Project/ga-ezgif.com-video-to-gif-converter.gif)
*   **Nhận xét về hiệu suất (8-Puzzle):**
    *   **Tính tối ưu:** Không. GA không đảm bảo tìm ra trạng thái đích tối ưu (nếu có nhiều) và đường đi tìm được bởi A* sau đó cũng chỉ tối ưu cho trạng thái đích *mà GA tìm được*, không nhất thiết là đường đi tối ưu tổng thể từ trạng thái ban đầu.
    *   **Tính đầy đủ:** Không đảm bảo. GA có thể hội tụ sớm về giải pháp dưới tối ưu hoặc không hội tụ nếu các tham số không phù hợp.
    *   **Độ phức tạp thời gian:** Có thể rất chậm, phụ thuộc nhiều vào kích thước quần thể, số thế hệ, cách thực hiện các toán tử lai ghép/đột biến. Việc chạy A* sau đó cũng tốn thêm thời gian.
    *   **Độ phức tạp không gian (bộ nhớ):** Cao. Cần lưu trữ toàn bộ quần thể các cá thể.

---

#### 6. Tìm kiếm Chùm tia Cục bộ (Local Beam Search)
*   **Mô tả:** Giữ lại `k` trạng thái tốt nhất (theo heuristic `h(n)`) tại mỗi bước duyệt. Bắt đầu với `k` trạng thái (có thể là `k` trạng thái khởi tạo hoặc `k` trạng thái kế tiếp của trạng thái khởi tạo). Từ `k` trạng thái này, sinh ra tất cả các trạng thái kế tiếp của chúng. Sau đó, từ *tất cả* các trạng thái kế tiếp này, chọn ra `k` trạng thái tốt nhất để tiếp tục cho vòng lặp sau. Thuật toán dừng khi một trong `k` trạng thái là trạng thái đích hoặc không thể tạo ra trạng thái tốt hơn.
*   **Minh họa:**
    *(Hiện chưa có GIF minh họa cho thuật toán này trong dự án)*
*   **Nhận xét về hiệu suất (8-Puzzle):**
    *   **Tính tối ưu:** Không.
    *   **Tính đầy đủ:** Không. Nếu cả `k` trạng thái hiện tại đều dẫn vào ngõ cụt hoặc cực tiểu địa phương mà không phải đích, thuật toán sẽ thất bại. Nó cũng có thể mất đi sự đa dạng nếu `k` trạng thái tốt nhất tập trung ở một vùng của không gian tìm kiếm.
    *   **Độ phức tạp thời gian:** Phụ thuộc vào `k` và số lượng trạng thái con sinh ra ở mỗi bước.
    *   **Độ phức tạp không gian (bộ nhớ):** O(k*b) hoặc O(k), tùy cách cài đặt. Bộ nhớ bị giới hạn bởi `k`, thường thấp hơn các thuật toán duyệt toàn bộ như A* hay BFS. Stochastic Beam Search (chọn `k` trạng thái kế tiếp theo xác suất dựa trên heuristic) có thể tăng tính đa dạng.

---

### 2.4. Các Thuật Toán Cho Môi Trường Phức Tạp (Complex Environments)

Phần này xem xét các tình huống tìm kiếm mà tác tử (agent) không có thông tin đầy đủ về môi trường hoặc trạng thái của chính nó.

#### 1. Tìm kiếm không cảm biến (Sensorless Search)
*   **Mô tả:** Áp dụng khi tác tử không biết chắc chắn trạng thái ban đầu của mình là gì, mà chỉ biết nó thuộc một tập hợp các trạng thái có thể, gọi là **trạng thái niềm tin (belief state)**. Mục tiêu là tìm một **kế hoạch phù hợp (conformant plan)** - một chuỗi hành động duy nhất mà khi thực hiện sẽ chắc chắn dẫn tác tử đến trạng thái đích, bất kể trạng thái ban đầu thực sự là gì trong tập hợp trạng thái niềm tin ban đầu. Việc tìm kiếm diễn ra trong không gian của các trạng thái niềm tin. Một cách phổ biến là áp dụng BFS trên không gian này:
    *   Trạng thái ban đầu là belief state ban đầu.
    *   Hành động `a` áp dụng lên belief state `b` sẽ tạo ra belief state mới chứa tất cả các trạng thái có thể đạt được bằng cách thực hiện `a` từ *bất kỳ* trạng thái nào trong `b`.
    *   Mục tiêu là đạt được một belief state mà tất cả các trạng thái trong đó đều là trạng thái đích.
*   **Lời giải (Solution):** Một chuỗi hành động (plan) đảm bảo đạt đích từ bất kỳ trạng thái nào trong belief state ban đầu.
*   **Minh họa (Áp dụng BFS trên không gian belief state):**
    ![BFS Sensorless Animation](https://raw.githubusercontent.com/buihaiduongdev/project-images/main/AI-Personal-Project/sl-ezgif.com-video-to-gif-converter.gif)
*   **Nhận xét về hiệu suất (8-Puzzle):**
    *   **Tính tối ưu:** Nếu dùng BFS trên không gian belief state, nó sẽ tìm ra conformant plan ngắn nhất (nếu tồn tại).
    *   **Tính đầy đủ:** Có. Nếu tồn tại một conformant plan, BFS trên không gian belief state sẽ tìm thấy nó.
    *   **Độ phức tạp thời gian:** Cực kỳ cao. Số lượng belief state có thể lớn hơn rất nhiều so với số lượng trạng thái vật lý (lên đến 2<sup>N</sup> với N trạng thái vật lý). Tìm kiếm trong không gian này thường rất tốn kém.
    *   **Độ phức tạp không gian (bộ nhớ):** Cực kỳ cao. Phải lưu trữ các belief state trong hàng đợi, mỗi belief state có thể chứa nhiều trạng thái vật lý.

---

### 2.5 Bài Toán Thỏa Mãn Ràng Buộc (Constraint Satisfaction Problems - CSPs)

Bài toán 8-Puzzle về bản chất là một bài toán tìm kiếm đường đi trong không gian trạng thái. Tuy nhiên, các kỹ thuật giải CSP, đặc biệt là quay lui, cũng có thể được xem xét, mặc dù việc mô hình hóa nó trực tiếp như một CSP tĩnh không phải là cách tiếp cận tự nhiên hay hiệu quả nhất để tìm đường đi. Các thuật toán quay lui là phương pháp nền tảng để giải CSP.

**Mô hình hóa (ví dụ, không tối ưu cho tìm đường đi):**
*   **Biến (Variables):** Vị trí của mỗi ô số, ví dụ: `Pos(Tile1), Pos(Tile2), ..., Pos(Tile8), Pos(Blank)`.
*   **Miền giá trị (Domains):** Tập 9 ô trên bảng, ví dụ: `{(0,0), (0,1), ..., (2,2)}`.
*   **Ràng buộc (Constraints):** `AllDifferent(Pos(Tile1), ..., Pos(Blank))`. Có thể thêm ràng buộc về trạng thái đích, nhưng việc diễn tả ràng buộc về *quá trình* di chuyển là phức tạp trong mô hình CSP tĩnh.

**Lời giải (Solution):** Một phép gán giá trị (vị trí) cho tất cả các biến (ô số) sao cho tất cả các ràng buộc được thỏa mãn (tức là đạt được cấu hình đích). Thuật toán quay lui cố gắng xây dựng phép gán này. Khi áp dụng cho bài toán *tìm đường đi* 8-puzzle, các thuật toán quay lui hoạt động tương tự như tìm kiếm theo chiều sâu.

---

#### 1. Quay lui (Backtracking - BT)
*   **Mô tả:** Là một cải tiến của DFS để giải các bài toán tìm kiếm, đặc biệt là CSP. Nó duyệt cây tìm kiếm theo chiều sâu. Tại mỗi nút, nó kiểm tra xem liệu có thể hoàn thành lời giải từ nút đó hay không. Nếu không (ví dụ, vi phạm ràng buộc trong CSP, hoặc đạt giới hạn độ sâu/gặp ngõ cụt trong tìm đường đi), nó sẽ quay lui (backtrack) lên nút cha và thử một nhánh khác. Trong ngữ cảnh tìm đường đi 8-puzzle, nó thực hiện một hành động, đi sâu, nếu không đạt đích hoặc gặp trạng thái đã thăm/giới hạn độ sâu thì quay lại và thử hành động khác.
*   **Minh họa:**
    ![Backtracking Animation](https://raw.githubusercontent.com/buihaiduongdev/project-images/main/AI-Personal-Project/bt-ezgif.com-video-to-gif-converter.gif)
*   **Nhận xét về hiệu suất (8-Puzzle - khi dùng để tìm đường đi):**
    *   **Tính tối ưu:** Không. Giống như DFS, không đảm bảo tìm đường đi ngắn nhất.
    *   **Tính đầy đủ:** Không (nếu không có giới hạn độ sâu hoặc kiểm tra chu trình/trạng thái đã thăm).
    *   **Độ phức tạp thời gian:** O(b<sup>m</sup>). Có thể chậm.
    *   **Độ phức tạp không gian (bộ nhớ):** O(b*m). Yêu cầu bộ nhớ thấp. Về cơ bản, hoạt động giống DFS khi áp dụng cho bài toán tìm đường đi đơn thuần.

---

#### 2. Quay lui CSP (CSP Backtracking - CSP BT)
*   **Mô tả:** Áp dụng thuật toán quay lui cơ bản trong khuôn khổ giải bài toán thỏa mãn ràng buộc. Nó gán giá trị cho các biến một cách tuần tự và tại mỗi bước kiểm tra xem phép gán hiện tại có vi phạm ràng buộc nào không. Nếu có vi phạm hoặc không thể gán tiếp, nó quay lui. Khi áp dụng trực tiếp vào việc *tìm đường đi* trong 8-puzzle mà không có các kỹ thuật tăng tốc CSP chuyên dụng (như kiểm tra trước - forward checking, duy trì nhất quán cung - arc consistency, sắp xếp biến/giá trị), hoạt động của nó rất giống với Backtracking thông thường hoặc DFS.
*   **Minh họa:**
    ![CSP Backtracking Animation](https://raw.githubusercontent.com/buihaiduongdev/project-images/main/AI-Personal-Project/csp-ezgif.com-video-to-gif-converter.gif)
*   **Nhận xét về hiệu suất (8-Puzzle - khi dùng để tìm đường đi):**
    *   **Tính tối ưu:** Không.
    *   **Tính đầy đủ:** Không (tương tự BT/DFS).
    *   **Độ phức tạp thời gian:** Chậm, O(b<sup>m</sup>).
    *   **Độ phức tạp không gian (bộ nhớ):** Thấp, O(b*m). Hiệu quả thực sự của cách tiếp cận CSP cho các bài toán phù hợp đến từ việc kết hợp quay lui với các kỹ thuật truyền bá ràng buộc và heuristic, điều này không được thể hiện rõ khi chỉ áp dụng quay lui cơ bản cho bài toán tìm đường đi 8-puzzle.

---

### 2.6 Học Tăng Cường (Reinforcement Learning - RL)

Học tăng cường là một lĩnh vực của học máy, nơi một tác tử (agent) tương tác với một môi trường và học cách hành động thông qua thử và sai để tối đa hóa một tín hiệu phần thưởng (reward) tích lũy theo thời gian.

**Mô hình hóa 8-Puzzle cho RL (trong khuôn khổ Markov Decision Process - MDP):**
*   **Trạng thái (State - S):** Tập hợp tất cả các cấu hình có thể của bảng 3x3 (khoảng 9!/2 = 181,440 trạng thái).
*   **Hành động (Action - A):** Tập các hành động có thể thực hiện từ một trạng thái (di chuyển ô trống U, D, L, R, nếu hợp lệ).
*   **Hàm chuyển đổi (Transition Model - P(s' | s, a)):** Xác suất chuyển đến trạng thái `s'` khi thực hiện hành động `a` tại trạng thái `s`. Trong 8-puzzle, môi trường là tất định, nên P(s' | s, a) = 1 nếu `s'` là kết quả của `a` tại `s`, và bằng 0 nếu khác.
*   **Hàm phần thưởng (Reward Function - R(s, a, s')):** Phần thưởng nhận được khi chuyển từ `s` đến `s'` bằng hành động `a`. Ví dụ: +100 khi đạt trạng thái đích, -1 cho mỗi bước di chuyển (để khuyến khích đường đi ngắn), -10 nếu thực hiện hành động không hợp lệ.
*   **Chính sách (Policy - π(s)):** Một hàm ánh xạ từ trạng thái sang hành động, chỉ định hành động mà tác tử nên thực hiện tại mỗi trạng thái. Mục tiêu là học chính sách tối ưu π*.
*   **Hàm giá trị (Value Function):**
    *   **V(s):** Giá trị kỳ vọng (tổng phần thưởng chiết khấu trong tương lai) khi bắt đầu từ trạng thái `s` và tuân theo một chính sách π.
    *   **Q(s, a):** Giá trị kỳ vọng khi thực hiện hành động `a` tại trạng thái `s`, và sau đó tuân theo chính sách π.

**Lời giải (Solution):** Chính sách tối ưu π* chỉ dẫn cách hành động tại mọi trạng thái để tối đa hóa phần thưởng kỳ vọng dài hạn. Khi có π*, tác tử có thể đi từ trạng thái ban đầu đến trạng thái đích bằng cách luôn chọn hành động `a = π*(s)` tại mỗi trạng thái `s`.

---

#### 1. Q-Learning (QL)
*   **Mô tả:** Là một thuật toán RL **không cần mô hình (model-free)** và **ngoài chính sách (off-policy)**. Nó học trực tiếp hàm giá trị hành động tối ưu Q*(s, a) mà không cần biết mô hình chuyển đổi P hay hàm phần thưởng R một cách tường minh. Tác tử tương tác với môi trường, thử các hành động (cân bằng giữa **thăm dò - exploration** để khám phá và **khai thác - exploitation** để chọn hành động tốt nhất đã biết) và cập nhật giá trị Q của cặp (trạng thái, hành động) đã thực hiện dựa trên phần thưởng nhận được và ước lượng giá trị tối đa của trạng thái kế tiếp, thông qua phương trình cập nhật Bellman:
    `Q(s, a) ← Q(s, a) + α [ R + γ max<sub>a'</sub> Q(s', a') - Q(s, a) ]`
    Trong đó: `α` là tốc độ học (learning rate), `γ` là hệ số chiết khấu (discount factor).
    *Lưu ý:* Quá trình huấn luyện (học Q-table) thường diễn ra qua hàng nghìn hoặc hàng triệu lượt tương tác (episodes) và không được hiển thị trong animation. Animation chỉ thể hiện việc *sử dụng* Q-table đã học (chế độ khai thác hoàn toàn) để tìm đường đi từ trạng thái đầu đến đích.
*   **Minh họa:**
    ![Q-Learning Animation](https://raw.githubusercontent.com/buihaiduongdev/project-images/main/AI-Personal-Project/ql-ezgif.com-video-to-gif-converter.gif)
*   **Nhận xét về hiệu suất (8-Puzzle):**
    *   **Tính tối ưu:** Có thể hội tụ đến chính sách tối ưu (dẫn đến đường đi ngắn nhất nếu hàm thưởng được thiết kế phù hợp) nếu các tham số (α, γ, chiến lược thăm dò ε-greedy) được chọn đúng và tác tử được huấn luyện đủ lâu (thăm mọi cặp (s, a) đủ số lần).
    *   **Tính đầy đủ:** Có (nếu hội tụ).
    *   **Độ phức tạp thời gian:** Thời gian **huấn luyện** rất lâu, đòi hỏi nhiều lượt tương tác với môi trường. Tuy nhiên, thời gian **sử dụng** chính sách đã học để tìm đường đi (tra cứu Q-table và chọn hành động có Q-value cao nhất) là rất nhanh, O(d) với d là độ dài đường đi.
    *   **Độ phức tạp không gian (bộ nhớ):** Rất cao. Cần lưu trữ Q-table, có kích thước bằng (số trạng thái * số hành động). Với ~181K trạng thái và tối đa 4 hành động, Q-table cho 8-puzzle là khá lớn đối với phương pháp học dạng bảng (tabular Q-learning). Các phương pháp xấp xỉ hàm (function approximation) như Deep Q-Networks (DQN) có thể giải quyết vấn đề bộ nhớ cho các không gian trạng thái lớn hơn nhiều.

---

## 3. So Sánh Hiệu Suất Các Thuật Toán (Tóm tắt)

Bảng dưới đây tóm tắt các đặc tính chính của các thuật toán đã triển khai khi áp dụng cho bài toán 8-puzzle:

| Thuật Toán                  | Loại                 | Đảm Bảo Tối Ưu (Đường đi ngắn nhất) | Tính Đầy Đủ | Bộ Nhớ Sử Dụng | Tốc Độ Thực Thi (Tìm lời giải) | Ghi Chú                                                          |
| :-------------------------- | :------------------- | :---------------------------------- | :---------- | :-------------- | :----------------------------- | :--------------------------------------------------------------- |
| **BFS**                     | Uninformed           | Có                                  | Có          | Cao (O(b<sup>d</sup>))    | Chậm (O(b<sup>d</sup>))                  | Đảm bảo tối ưu nhưng tốn bộ nhớ/thời gian.                       |
| **DFS**                     | Uninformed           | Không                               | Không*      | Thấp (O(bm))    | Nhanh/Chậm (O(b<sup>m</sup>))            | Tốn ít bộ nhớ, không tối ưu, cần giới hạn độ sâu/kiểm tra lặp.    |
| **IDDFS**                   | Uninformed           | Có                                  | Có          | Thấp (O(bd))    | Trung bình (O(b<sup>d</sup>))        | Kết hợp tốt nhất của BFS (tối ưu) và DFS (bộ nhớ).              |
| **UCS**                     | Uninformed           | Có                                  | Có          | Cao (O(b<sup>d</sup>))    | Chậm (O(b<sup>d</sup>))                  | Tương tự BFS khi chi phí bước là 1.                              |
| **A\***                     | Informed             | Có**                                | Có          | Cao             | Nhanh                          | Rất hiệu quả với heuristic tốt, nhưng tốn bộ nhớ.                |
| **IDA\***                   | Informed             | Có**                                | Có          | Thấp (O(bd))    | Trung bình                   | Phiên bản tiết kiệm bộ nhớ của A*.                               |
| **Greedy Best-First**       | Informed             | Không                               | Không*      | Trung bình/Cao  | Rất nhanh (thường)           | Nhanh tìm giải pháp nhưng không tối ưu, có thể bị kẹt.           |
| **Local Beam Search**       | Informed             | Không                               | Không       | Trung bình (k)  | Trung bình                   | Giữ k trạng thái tốt nhất, dễ mất đa dạng, cần chọn k.         |
| **Hill Climbing (các loại)**| Local Search         | Không                               | Không       | Rất thấp (O(1)) | Rất nhanh                    | Nhanh, ít bộ nhớ, nhưng dễ bị kẹt ở cực tiểu địa phương.          |
| **Simulated Annealing**     | Local Search         | Không (Xác suất cao)                | Có (Xác suất)| Rất thấp (O(1)) | Trung bình                   | Có khả năng thoát cực tiểu, phụ thuộc lịch trình làm nguội.     |
| **Genetic Algorithm***      | Local Search         | Không                               | Không       | Cao             | Chậm                         | Dựa trên quần thể, cần A* để tìm path, phụ thuộc tham số.        |
| **Sensorless Search (BFS)** | Complex Environments | Có (Plan ngắn nhất)                 | Có          | Rất cao         | Rất chậm                     | Giải quyết bất định trạng thái, hoạt động trên belief state.      |
| **Backtracking (BT)**       | CSPs / Uninformed    | Không                               | Không*      | Thấp (O(bm))    | Chậm (O(b<sup>m</sup>))                  | Tương tự DFS cho tìm đường đi.                                   |
| **CSP Backtracking**        | CSPs                 | Không                               | Không*      | Thấp            | Chậm                         | Như BT khi áp dụng đơn giản cho tìm đường đi.                    |
| **Q-Learning***             | Reinforcement Learning| Có (Chính sách tối ưu)             | Có          | Rất cao (Q-table)| Huấn luyện: Rất chậm; Sử dụng: Nhanh | Cần huấn luyện dài, tốn bộ nhớ, nhưng sử dụng nhanh sau huấn luyện. |

**Chú thích bảng:**
*   `*`: Không đầy đủ nếu không có kiểm tra trạng thái đã thăm / giới hạn độ sâu. Tính đầy đủ của Greedy/Local Search cũng phụ thuộc vào việc có bị kẹt hay không.
*   `**`: Đảm bảo tối ưu nếu heuristic là chấp nhận được/nhất quán (ví dụ: Manhattan Distance được sử dụng trong dự án này).
*   `***`: GA và QL trong dự án này có cách tiếp cận hơi khác: GA tìm trạng thái đích rồi dùng A* tìm đường đi. QL học chính sách, sau đó dùng chính sách để tạo đường đi. Tốc độ/Bộ nhớ/Tối ưu phản ánh cả quá trình. Tốc độ thực thi của QL là tốc độ *sau khi* đã huấn luyện.

---

## 4. Kết Luận

Dự án đã triển khai và minh họa thành công một phổ rộng các thuật toán tìm kiếm và học máy từ cơ bản đến nâng cao trong lĩnh vực Trí tuệ Nhân tạo để giải quyết bài toán 8-puzzle. Việc trực quan hóa quá trình giải bằng Pygame và so sánh các đặc tính về tính tối ưu, tính đầy đủ, độ phức tạp thời gian và không gian của từng thuật toán cung cấp một cái nhìn sâu sắc và thực tế. Nó cho thấy rõ sự đánh đổi giữa các yếu tố này: các thuật toán không thông tin như BFS/IDDFS đảm bảo tối ưu nhưng có thể chậm hoặc tốn bộ nhớ; các thuật toán có thông tin như A*/IDA* hiệu quả hơn nhờ heuristic nhưng vẫn có thể tốn bộ nhớ (A*) hoặc thời gian (IDA*); các thuật toán tìm kiếm cục bộ nhanh và tiết kiệm bộ nhớ nhưng không đảm bảo tối ưu/đầy đủ; trong khi các phương pháp phức tạp hơn như Sensorless Search hay Reinforcement Learning giải quyết các khía cạnh khác của bài toán nhưng đi kèm với chi phí tính toán cao. Tổng hợp lại, dự án là một tài liệu học tập hữu ích, giúp hiểu rõ hơn về nguyên lý hoạt động và phạm vi ứng dụng của các kỹ thuật tìm kiếm AI khác nhau.

---
