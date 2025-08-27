# Web Xanh: Chung Tay Vì Một Tương Lai Bền Vững

![Web Xanh Logo](https://raw.githubusercontent.com/your-username/web-xanh/main/static/icons/icon-512x512.png)

## Giới Thiệu

"Web Xanh" là một ứng dụng web tương tác được phát triển nhằm nâng cao nhận thức và khuyến khích hành động bảo vệ môi trường. Ứng dụng này kết hợp các tính năng giáo dục, trò chơi tương tác và công cụ tìm kiếm thông tin để tạo ra một trải nghiệm học tập và giải trí toàn diện.

Được xây dựng với Flask (Python) ở backend và HTML/CSS/JavaScript ở frontend, "Web Xanh" cũng được tối ưu hóa như một Progressive Web App (PWA) để mang lại trải nghiệm giống ứng dụng di động trên mọi thiết bị.

## Tính Năng Nổi Bật

*   **Trang Chủ:** Hiển thị thông tin về các loại ô nhiễm môi trường chính và tác hại của chúng.
*   **Hệ Thống Tài Khoản Người Dùng:** Cho phép nhiều người dùng đăng ký, đăng nhập và quản lý phiên cá nhân.
*   **Game "Nhặt Rác Thải Dưới Đại Dương":** Trò chơi tương tác giáo dục nơi người chơi thu gom rác thải dưới biển và trả lời các câu hỏi môi trường.
*   **Game "Thu Thập Chai Nhựa":** Thử thách tốc độ với bot AI và bảng xếp hạng.
*   **Game "Phân Loại Rác Thông Minh":** Hướng dẫn phân loại rác đúng cách với AI hỗ trợ.
*   **AI Tư Vấn Môi Trường:** Chatbot thông minh trả lời các câu hỏi liên quan đến môi trường.
*   **DIY Tái Chế Sáng Tạo:** Cung cấp các video hướng dẫn tái chế rác thải thành đồ dùng hữu ích.
*   **Tìm Kiếm Video DIY:** Cho phép người dùng tìm kiếm các video hướng dẫn tái chế theo sở thích cá nhân.
*   **Progressive Web App (PWA):** Trải nghiệm như ứng dụng di động với splash screen, hoạt động offline và cài đặt trực tiếp từ trình duyệt.

## Công Nghệ Sử Dụng

*   **Backend:** Python, Flask, Flask-SQLAlchemy, Flask-Login, Flask-WTF
*   **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5
*   **Database:** SQLite (mặc định cho phát triển, khuyến nghị Cloud SQL cho sản xuất)
*   **PWA:** Web App Manifest, Service Worker
*   **Deployment:** Docker, Google Cloud Build, Google Cloud Run

## Cài Đặt và Chạy Ứng Dụng Cục Bộ

Để chạy ứng dụng "Web Xanh" trên máy tính cục bộ của bạn, hãy làm theo các bước sau:

### Yêu Cầu

*   Python 3.8+
*   pip (trình quản lý gói Python)

### Các Bước

1.  **Clone Repository:**
    ```bash
    git clone https://github.com/your-username/web-xanh.git
    cd web-xanh/src
    ```
    *(Lưu ý: Thay `your-username` bằng tên người dùng GitHub của bạn sau khi bạn đã đẩy mã nguồn lên.)*

2.  **Tạo Môi Trường Ảo (Virtual Environment):**
    ```bash
    python -m venv venv
    ```

3.  **Kích Hoạt Môi Trường Ảo:**
    *   **Trên Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    *   **Trên macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

4.  **Cài Đặt Các Thư Viện Phụ Thuộc:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Khởi Tạo Cơ Sở Dữ Liệu:**
    Ứng dụng sử dụng SQLite. Khi bạn chạy ứng dụng lần đầu, file `site.db` sẽ được tạo tự động. Bạn có thể cần tạo các bảng cơ sở dữ liệu bằng cách chạy ứng dụng một lần hoặc sử dụng Flask-Migrate (nếu được cấu hình).

6.  **Chạy Ứng Dụng Flask:**
    ```bash
    flask run
    ```

7.  **Truy Cập Ứng Dụng:**
    Mở trình duyệt web của bạn và truy cập `http://127.0.0.1:5000` (hoặc cổng mà Flask hiển thị).

## Triển Khai Lên Google Cloud Platform (GCP)

Ứng dụng này được cấu hình sẵn để triển khai lên Google Cloud Run bằng Google Cloud Build. Bạn sẽ cần một tài khoản GCP và `gcloud CLI` đã được cài đặt.

### Các Bước Triển Khai

1.  **Chuẩn Bị Dự Án GCP:**
    *   Tạo hoặc chọn một dự án GCP.
    *   Kích hoạt các API cần thiết: Cloud Run API, Cloud Build API, Container Registry API.

2.  **Đẩy Mã Nguồn Lên GitHub:**
    Bạn cần đẩy mã nguồn này lên một repository GitHub của riêng bạn.

3.  **Kết Nối GitHub Với Cloud Build:**
    *   Trong GCP Console, điều hướng đến **Cloud Build > Triggers**.
    *   Nhấp vào **CONNECT REPOSITORY** và làm theo hướng dẫn để kết nối tài khoản GitHub của bạn và chọn repository `web-xanh`.
    *   Cấu hình trigger để chạy build khi có commit mới vào nhánh `main` (hoặc `master`). Chọn loại build là `Dockerfile` hoặc `Cloud Build configuration file` và trỏ đến `cloudbuild.yaml`.

4.  **Triển Khai Thủ Công (Nếu không dùng trigger):**
    Bạn có thể triển khai thủ công bằng cách chạy lệnh sau từ thư mục gốc của dự án (nơi chứa `cloudbuild.yaml`):
    ```bash
    gcloud builds submit --config cloudbuild.yaml --project YOUR_PROJECT_ID
    ```
    Thay `YOUR_PROJECT_ID` bằng ID dự án GCP của bạn.

5.  **Truy Cập Ứng Dụng Đã Triển Khai:**
    Sau khi triển khai thành công, Cloud Build sẽ cung cấp một URL dịch vụ Cloud Run. Bạn có thể truy cập ứng dụng của mình thông qua URL này.

### Lưu Ý Về Cơ Sở Dữ Liệu

Ứng dụng sử dụng SQLite (`site.db`) theo mặc định. Đối với môi trường sản xuất trên Cloud Run, **SQLite không được khuyến nghị** vì Cloud Run là môi trường không trạng thái. Để có cơ sở dữ liệu bền vững và có khả năng mở rộng, bạn nên di chuyển sang **Cloud SQL (PostgreSQL hoặc MySQL)** hoặc một dịch vụ cơ sở dữ liệu được quản lý khác.

Bạn sẽ cần cập nhật chuỗi kết nối cơ sở dữ liệu trong `main.py` và cấu hình dịch vụ Cloud Run để kết nối với Cloud SQL instance của bạn. Tham khảo tài liệu GCP về cách kết nối Cloud Run với Cloud SQL để biết thêm chi tiết.

## Đóng Góp

Chúng tôi hoan nghênh mọi đóng góp để cải thiện ứng dụng "Web Xanh". Nếu bạn có ý tưởng, báo cáo lỗi hoặc muốn đóng góp mã, vui lòng mở một issue hoặc gửi pull request trên GitHub.

## Giấy Phép

Dự án này được cấp phép theo Giấy phép MIT. Xem file `LICENSE` để biết thêm chi tiết.

## Liên Hệ

Nếu bạn có bất kỳ câu hỏi nào, vui lòng liên hệ qua GitHub Issues.

---

**Bản quyền © 2025 Manus AI. Mọi quyền được bảo lưu.**

