# Hướng Dẫn Triển Khai Ứng Dụng "Web Xanh" Lên Google Cloud Platform (GCP)

**Tác giả:** Manus AI

## Giới Thiệu

Chào mừng bạn đến với hướng dẫn chi tiết về cách triển khai ứng dụng "Web Xanh" lên Google Cloud Platform (GCP). "Web Xanh" là một ứng dụng web tương tác được phát triển bằng Flask (Python) ở backend và HTML/CSS/JavaScript ở frontend, với các tính năng như hệ thống tài khoản người dùng, trò chơi giáo dục môi trường (ví dụ: "Nhặt Rác Thải Dưới Đại Dương", "Thu Thập Chai Nhựa"), và tìm kiếm video DIY tái chế. Ứng dụng này cũng được tối ưu hóa như một Progressive Web App (PWA) để mang lại trải nghiệm giống ứng dụng di động.

Việc triển khai lên GCP sẽ giúp ứng dụng của bạn có thể truy cập công khai, ổn định, có khả năng mở rộng và bảo mật cao. Hướng dẫn này sẽ tập trung vào việc sử dụng Cloud Run, một nền tảng điện toán được quản lý hoàn toàn cho phép bạn chạy các vùng chứa không trạng thái thông qua các yêu cầu HTTP. Cloud Run lý tưởng cho các ứng dụng web như "Web Xanh" vì nó tự động mở rộng quy mô từ 0 đến hàng nghìn phiên bản dựa trên lưu lượng truy cập, và bạn chỉ phải trả tiền cho tài nguyên bạn sử dụng.

### Mục Tiêu Của Hướng Dẫn

Sau khi hoàn thành hướng dẫn này, bạn sẽ có thể:

1.  Thiết lập môi trường GCP cần thiết.
2.  Đóng gói ứng dụng "Web Xanh" thành một Docker image.
3.  Triển khai Docker image lên Cloud Run.
4.  Cấu hình cơ sở dữ liệu (SQLite ban đầu, có thể nâng cấp lên Cloud SQL).
5.  Truy cập ứng dụng "Web Xanh" đã được triển khai công khai.

### Yêu Cầu Tiên Quyết

Để thực hiện theo hướng dẫn này, bạn cần có:

*   **Tài khoản Google Cloud Platform:** Đảm bảo bạn đã kích hoạt tài khoản và có quyền tạo dự án, kích hoạt API và quản lý tài nguyên. Nếu chưa có, bạn có thể đăng ký dùng thử miễn phí với tín dụng 300 USD [1].
*   **Dự án GCP:** Một dự án GCP đã được tạo và chọn làm dự án hiện tại.
*   **Cloud SDK (gcloud CLI):** Đã cài đặt và cấu hình `gcloud CLI` trên máy tính cục bộ của bạn. Bạn có thể tải xuống và cài đặt theo hướng dẫn chính thức của Google [2].
*   **Docker:** Đã cài đặt Docker Desktop hoặc Docker Engine trên máy tính cục bộ của bạn để xây dựng và kiểm tra Docker image cục bộ (tùy chọn, Cloud Build có thể thực hiện việc này).
*   **Mã nguồn ứng dụng "Web Xanh":** Bạn đã có mã nguồn của ứng dụng "Web Xanh" (được cung cấp trong gói tải xuống).

---

## Bước 1: Chuẩn Bị Dự Án GCP

Trước khi triển khai ứng dụng, bạn cần đảm bảo dự án GCP của mình đã được thiết lập đúng cách và các API cần thiết đã được kích hoạt.

### 1.1. Chọn hoặc Tạo Dự Án GCP

Nếu bạn đã có một dự án GCP, hãy chọn nó. Nếu không, hãy tạo một dự án mới. Bạn có thể thực hiện việc này thông qua giao diện điều khiển GCP (GCP Console) hoặc `gcloud CLI`.

**Sử dụng GCP Console:**

1.  Truy cập [GCP Console](https://console.cloud.google.com/).
2.  Ở đầu trang, nhấp vào trình chọn dự án (thường hiển thị tên dự án hiện tại hoặc "My First Project").
3.  Trong hộp thoại "Select a project", nhấp vào "NEW PROJECT".
4.  Nhập tên dự án (ví dụ: `web-xanh-project`) và chọn tổ chức/vị trí thanh toán nếu có. Nhấp vào "CREATE".
5.  Sau khi dự án được tạo, đảm bảo bạn đã chọn dự án đó trong trình chọn dự án.

**Sử dụng gcloud CLI:**

Để tạo dự án mới:

```bash
gcloud projects create YOUR_PROJECT_ID --name="Web Xanh Project"
```

Thay `YOUR_PROJECT_ID` bằng một ID dự án duy nhất (ví dụ: `web-xanh-2025`). ID dự án phải là duy nhất trên toàn cầu và không thể thay đổi sau khi tạo.

Để đặt dự án vừa tạo làm dự án hiện tại:

```bash
gcloud config set project YOUR_PROJECT_ID
```

### 1.2. Kích Hoạt Các API Cần Thiết

Ứng dụng "Web Xanh" và quy trình triển khai sẽ yêu cầu một số API của GCP. Bạn cần kích hoạt chúng cho dự án của mình.

**Các API cần kích hoạt:**

*   **Cloud Run API:** Để triển khai và quản lý các dịch vụ Cloud Run.
*   **Cloud Build API:** Để xây dựng Docker image từ mã nguồn của bạn.
*   **Container Registry API (hoặc Artifact Registry API):** Để lưu trữ Docker image của bạn.

**Sử dụng GCP Console:**

1.  Trong GCP Console, điều hướng đến "APIs & Services" > "Enabled APIs & services".
2.  Nhấp vào "+ ENABLE APIS AND SERVICES".
3.  Tìm kiếm và kích hoạt từng API một: "Cloud Run API", "Cloud Build API", "Container Registry API".

**Sử dụng gcloud CLI:**

```bash
gcloud services enable run.googleapis.com \
                       cloudbuild.googleapis.com \
                       containerregistry.googleapis.com
```

---

## Bước 2: Chuẩn Bị Mã Nguồn Ứng Dụng "Web Xanh"

Bạn đã có mã nguồn của ứng dụng "Web Xanh". Trong gói mã nguồn này, bạn sẽ tìm thấy các file quan trọng sau:

*   `main.py`: File chính của ứng dụng Flask.
*   `requirements.txt`: Danh sách các thư viện Python cần thiết.
*   `Dockerfile`: Hướng dẫn để xây dựng Docker image cho ứng dụng.
*   `cloudbuild.yaml`: Cấu hình cho Cloud Build để tự động xây dựng và triển khai.
*   Thư mục `templates/`: Chứa các file HTML (Jinja2 templates).
*   Thư mục `static/`: Chứa các file CSS, JavaScript, hình ảnh, icons.
*   Các file khác như `models.py`, `auth.py`, `ocean_cleanup_data.py`.

Đảm bảo tất cả các file này nằm trong cùng một thư mục gốc của dự án mà bạn sẽ tải lên GCP. Cấu trúc thư mục của bạn sẽ trông như sau:

```
web-xanh/
├── main.py
├── requirements.txt
├── Dockerfile
├── cloudbuild.yaml
├── models.py
├── auth.py
├── ocean_cleanup_data.py
├── templates/
│   ├── auth/
│   │   ├── login.html
│   │   └── register.html
│   ├── ... (các file html khác)
│   ├── games.html
│   ├── ocean_cleanup.html
│   ├── ...
├── static/
│   ├── css/
│   │   ├── style.css
│   │   └── pwa-enhanced.css
│   ├── js/
│   │   ├── script.js
│   │   ├── pwa-enhanced.js
│   │   ├── bottle_game.js
│   │   ├── ocean_cleanup.js
│   │   ├── video_search.js
│   │   └── waste_sorting.js
│   ├── images/
│   │   ├── ... (các hình ảnh)
│   ├── icons/
│   │   ├── ... (các icon PWA)
│   └── manifest.json
└── ... (các file khác)
```

**Lưu ý quan trọng về cơ sở dữ liệu:**

Ứng dụng "Web Xanh" hiện đang sử dụng SQLite làm cơ sở dữ liệu cục bộ (`site.db`). Đối với môi trường sản xuất trên Cloud Run, việc sử dụng SQLite không được khuyến khích vì Cloud Run là môi trường không trạng thái (stateless) và các thay đổi trên hệ thống file sẽ không được duy trì giữa các phiên bản hoặc khi ứng dụng được khởi động lại. 

Để có một cơ sở dữ liệu bền vững và có khả năng mở rộng, bạn nên di chuyển sang một dịch vụ cơ sở dữ liệu được quản lý như **Cloud SQL (PostgreSQL hoặc MySQL)** hoặc **Firestore/Datastore**. Hướng dẫn này sẽ tập trung vào việc triển khai ứng dụng như hiện tại với SQLite để đơn giản hóa, nhưng bạn cần lưu ý đây là một điểm cần nâng cấp cho môi trường sản xuất thực tế.

---

## Bước 3: Xây Dựng và Triển Khai Ứng Dụng Với Cloud Build

Cloud Build là một dịch vụ CI/CD của GCP cho phép bạn tự động xây dựng, kiểm thử và triển khai ứng dụng. Chúng ta sẽ sử dụng `cloudbuild.yaml` đã chuẩn bị để định nghĩa quy trình này.

### 3.1. Tải Mã Nguồn Lên GitHub

Để tích hợp tốt hơn với Cloud Build và quản lý phiên bản, bạn nên tải mã nguồn của mình lên một repository GitHub. Nếu bạn chưa có tài khoản GitHub, hãy tạo một tài khoản tại [github.com](https://github.com/).

1.  **Tạo một Repository mới trên GitHub:**
    *   Đăng nhập vào tài khoản GitHub của bạn.
    *   Nhấp vào biểu tượng dấu cộng (+) ở góc trên bên phải và chọn "New repository".
    *   Đặt tên cho repository (ví dụ: `web-xanh`). Đảm bảo nó là public hoặc private tùy theo nhu cầu của bạn.
    *   **Không** tích chọn "Add a README file", "Add .gitignore", hoặc "Choose a license" vì chúng ta đã có các file này trong mã nguồn.
    *   Nhấp vào "Create repository".

2.  **Khởi tạo Git repository cục bộ và đẩy mã nguồn lên GitHub:**
    Điều hướng đến thư mục gốc của dự án "Web Xanh" (`web-xanh/`) trên máy tính cục bộ của bạn. Đảm bảo bạn đã cài đặt Git trên máy tính.
    ```bash
    git init
    git add .
    git commit -m "Initial commit of Web Xanh application"
    git branch -M main
    git remote add origin https://github.com/YOUR_GITHUB_USERNAME/web-xanh.git
    git push -u origin main
    ```
    Thay `YOUR_GITHUB_USERNAME` bằng tên người dùng GitHub của bạn.

### 3.2. Kết Nối GitHub Với Google Cloud Build

Google Cloud Build có thể tự động xây dựng và triển khai ứng dụng của bạn mỗi khi có thay đổi trên repository GitHub. Đây là một quy trình CI/CD (Continuous Integration/Continuous Deployment) hiệu quả.

1.  **Truy cập Cloud Build trong GCP Console:**
    *   Trong GCP Console, điều hướng đến "Cloud Build" > "Triggers".
    *   Nhấp vào "CONNECT REPOSITORY".

2.  **Kết nối tài khoản GitHub của bạn:**
    *   Chọn "GitHub (Cloud Build GitHub App)" và nhấp vào "Continue".
    *   Bạn sẽ được chuyển hướng đến GitHub để cấp quyền cho Google Cloud Build. Cấp quyền truy cập vào repository `web-xanh` của bạn.

3.  **Cấu hình Trigger:**
    *   Sau khi kết nối thành công, bạn sẽ thấy danh sách các repository GitHub của mình. Chọn repository `web-xanh` và nhấp vào "CONNECT".
    *   Trên trang "Create trigger", cấu hình như sau:
        *   **Name:** `deploy-web-xanh` (hoặc tên bất kỳ bạn muốn)
        *   **Region:** Chọn region gần bạn (ví dụ: `us-central1`)
        *   **Event:** `Push to a branch`
        *   **Source:**
            *   **Repository:** Chọn `web-xanh`
            *   **Branch:** `^main$` (để trigger khi có push vào nhánh `main`)
        *   **Configuration:**
            *   **Type:** `Cloud Build configuration file`
            *   **Location:** `/cloudbuild.yaml` (đây là file chúng ta đã tạo trong mã nguồn)
    *   Nhấp vào "CREATE".

Bây giờ, mỗi khi bạn đẩy mã nguồn lên nhánh `main` trên GitHub, Cloud Build sẽ tự động kích hoạt một quá trình build và triển khai ứng dụng của bạn lên Cloud Run. Bạn có thể theo dõi tiến trình build trong "Cloud Build" > "History".

### 3.3. Triển Khai Thủ Công (Tùy chọn)

Nếu bạn muốn triển khai thủ công mà không cần kết nối GitHub hoặc để kiểm tra nhanh, bạn có thể chạy lệnh sau từ thư mục gốc của dự án "Web Xanh" (`web-xanh/`) trên máy tính cục bộ của bạn:

```bash
gcloud builds submit --config cloudbuild.yaml --project YOUR_PROJECT_ID
```

Thay `YOUR_PROJECT_ID` bằng ID dự án GCP của bạn.

**Giải thích lệnh:**

*   `gcloud builds submit`: Gửi một bản build đến Cloud Build.
*   `--config cloudbuild.yaml`: Chỉ định file cấu hình build.
*   `--project YOUR_PROJECT_ID`: Chỉ định dự án GCP mà bạn muốn thực hiện build.

Quá trình build có thể mất vài phút. Bạn sẽ thấy nhật ký build được in ra trên terminal. Sau khi build hoàn tất, bạn sẽ thấy một URL dịch vụ Cloud Run được cung cấp trong nhật ký.

### 3.4. Kiểm Tra Ứng Dụng Đã Triển Khai

Sau khi triển khai thành công, bạn có thể truy cập ứng dụng của mình thông qua URL được cung cấp bởi Cloud Run. URL này sẽ có dạng `https://web-xanh-YOUR_HASH-REGION.run.app`.

1.  Mở trình duyệt web và truy cập URL này.
2.  Kiểm tra các tính năng của ứng dụng: trang chủ, các game, tìm kiếm video, hệ thống đăng ký/đăng nhập.

**Lưu ý về tài khoản người dùng:**

Vì Cloud Run là stateless và chúng ta đang sử dụng SQLite, bất kỳ tài khoản người dùng nào bạn tạo trên ứng dụng đã triển khai sẽ không được duy trì nếu dịch vụ Cloud Run bị tắt hoặc khởi động lại. Để có hệ thống tài khoản người dùng bền vững, bạn cần cấu hình ứng dụng để sử dụng Cloud SQL hoặc một dịch vụ cơ sở dữ liệu khác.

---

## Bước 4: Cấu Hình Cơ Sở Dữ Liệu Bền Vững (Nâng Cao)

Như đã đề cập, SQLite không phù hợp cho môi trường sản xuất trên Cloud Run. Để có một cơ sở dữ liệu bền vững, bạn nên sử dụng Cloud SQL. Dưới đây là các bước tổng quan để di chuyển sang Cloud SQL (PostgreSQL hoặc MySQL).

### 4.1. Tạo Instance Cloud SQL

1.  Trong GCP Console, điều hướng đến "SQL".
2.  Nhấp vào "CREATE INSTANCE".
3.  Chọn loại cơ sở dữ liệu (ví dụ: PostgreSQL hoặc MySQL).
4.  Đặt ID instance (ví dụ: `web-xanh-db`), mật khẩu người dùng root, và chọn khu vực.
5.  Chọn cấu hình máy (machine type) và dung lượng lưu trữ phù hợp với nhu cầu của bạn.
6.  Nhấp vào "CREATE INSTANCE". Quá trình này có thể mất vài phút.

### 4.2. Cấu Hình Kết Nối Ứng Dụng Với Cloud SQL

Bạn cần cập nhật mã nguồn ứng dụng Flask của mình để kết nối với Cloud SQL thay vì SQLite. Điều này thường liên quan đến việc sử dụng `cloud-sql-python-connector` hoặc cấu hình biến môi trường `DATABASE_URL`.

**Ví dụ cấu hình cho PostgreSQL với SQLAlchemy:**

Trong `main.py` hoặc file cấu hình của bạn, bạn sẽ cần thay đổi chuỗi kết nối cơ sở dữ liệu. Cloud Run có thể kết nối với Cloud SQL thông qua Cloud SQL Proxy hoặc kết nối trực tiếp (nếu bạn cấu hình mạng phù hợp).

**Sử dụng Cloud SQL Proxy (được khuyến nghị cho Cloud Run):**

Cloud Run có tích hợp sẵn Cloud SQL Proxy. Bạn chỉ cần cấu hình dịch vụ Cloud Run để kết nối với instance Cloud SQL của bạn.

1.  **Cập nhật `main.py`:**
    Đảm bảo ứng dụng của bạn sử dụng biến môi trường để lấy chuỗi kết nối cơ sở dữ liệu. Ví dụ:
    ```python
    import os
    from flask_sqlalchemy import SQLAlchemy

    app = Flask(__name__)
    # Lấy chuỗi kết nối từ biến môi trường DATABASE_URL
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///site.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db = SQLAlchemy(app)
    ```

2.  **Cấu hình dịch vụ Cloud Run:**
    Khi triển khai hoặc cập nhật dịch vụ Cloud Run, bạn cần chỉ định kết nối đến instance Cloud SQL của mình.
    ```bash
    gcloud run deploy web-xanh \
      --image gcr.io/YOUR_PROJECT_ID/web-xanh:$COMMIT_SHA \
      --region us-central1 \
      --platform managed \
      --allow-unauthenticated \
      --add-cloudsql-instances YOUR_PROJECT_ID:YOUR_REGION:YOUR_CLOUD_SQL_INSTANCE_ID \
      --set-env-vars DATABASE_URL="postgresql://USER:PASSWORD@/DATABASE_NAME?host=/cloudsql/YOUR_PROJECT_ID:YOUR_REGION:YOUR_CLOUD_SQL_INSTANCE_ID"
    ```
    Thay thế các placeholder:
    *   `YOUR_PROJECT_ID`: ID dự án GCP của bạn.
    *   `YOUR_REGION`: Khu vực của instance Cloud SQL (ví dụ: `us-central1`).
    *   `YOUR_CLOUD_SQL_INSTANCE_ID`: ID của instance Cloud SQL bạn đã tạo.
    *   `USER`: Tên người dùng cơ sở dữ liệu (ví dụ: `postgres` hoặc `root`).
    *   `PASSWORD`: Mật khẩu người dùng cơ sở dữ liệu.
    *   `DATABASE_NAME`: Tên cơ sở dữ liệu trong instance Cloud SQL (ví dụ: `web_xanh_db`).

    Bạn cũng cần tạo cơ sở dữ liệu và các bảng trong Cloud SQL instance của mình. Điều này có thể được thực hiện bằng cách kết nối thủ công hoặc sử dụng Flask-Migrate.

### 4.3. Di Chuyển Dữ Liệu (Nếu Có)

Nếu bạn đã có dữ liệu trong file `site.db` (SQLite), bạn sẽ cần xuất dữ liệu đó và nhập vào Cloud SQL instance mới. Quá trình này phụ thuộc vào công cụ bạn sử dụng để xuất/nhập dữ liệu.

---

## Bước 5: Quản Lý và Giám Sát Ứng Dụng

Sau khi ứng dụng đã được triển khai, bạn có thể quản lý và giám sát nó thông qua GCP Console.

### 5.1. Xem Nhật Ký (Logs)

Cloud Run tích hợp với Cloud Logging. Bạn có thể xem nhật ký của ứng dụng để gỡ lỗi và giám sát hoạt động.

1.  Trong GCP Console, điều hướng đến "Cloud Run".
2.  Chọn dịch vụ `web-xanh` của bạn.
3.  Nhấp vào tab "Logs".

### 5.2. Quản Lý Phiên Bản (Revisions)

Cloud Run tự động tạo một phiên bản mới (revision) mỗi khi bạn triển khai một Docker image mới. Bạn có thể quản lý các phiên bản này, chuyển đổi lưu lượng truy cập giữa chúng, hoặc quay lại một phiên bản cũ.

1.  Trong GCP Console, điều hướng đến "Cloud Run".
2.  Chọn dịch vụ `web-xanh` của bạn.
3.  Nhấp vào tab "Revisions".

### 5.3. Cấu Hình Tên Miền Tùy Chỉnh (Custom Domains)

Để ứng dụng của bạn có một URL dễ nhớ hơn (ví dụ: `app.yourdomain.com`), bạn có thể cấu hình tên miền tùy chỉnh.

1.  Trong GCP Console, điều hướng đến "Cloud Run".
2.  Chọn dịch vụ `web-xanh` của bạn.
3.  Nhấp vào tab "Custom domains".
4.  Nhấp vào "ADD MAPPED DOMAIN" và làm theo hướng dẫn để xác minh tên miền và tạo các bản ghi DNS cần thiết.

---

## Kết Luận

Bạn đã hoàn thành việc triển khai ứng dụng "Web Xanh" lên Google Cloud Platform bằng Cloud Run. Ứng dụng của bạn hiện đã có thể truy cập công khai, có khả năng mở rộng và được quản lý bởi Google. Hãy nhớ rằng việc di chuyển sang một cơ sở dữ liệu bền vững như Cloud SQL là rất quan trọng cho môi trường sản xuất thực tế.

Chúc mừng bạn đã hoàn thành dự án này! Nếu có bất kỳ câu hỏi nào, đừng ngần ngại tìm kiếm thêm tài liệu hoặc hỏi cộng đồng GCP.

## Tài Liệu Tham Khảo

[1] Google Cloud Free Tier: [https://cloud.google.com/free](https://cloud.google.com/free)
[2] Cài đặt Google Cloud SDK: [https://cloud.google.com/sdk/docs/install](https://cloud.google.com/sdk/docs/install)
[3] Triển khai ứng dụng Python lên Cloud Run: [https://cloud.google.com/run/docs/deploying/python](https://cloud.google.com/run/docs/deploying/python)
[4] Kết nối Cloud Run với Cloud SQL: [https://cloud.google.com/sql/docs/mysql/connect-run](https://cloud.google.com/sql/docs/mysql/connect-run)

---

**Bản quyền © 2025 Manus AI. Mọi quyền được bảo lưu.**

