# Hệ thống Quản lý Nhân sự cơ bản

Đây là một ứng dụng quản lý nhân sự cơ bản, được phát triển bằng **Python** và sử dụng cơ sở dữ liệu **MongoDB** để lưu trữ dữ liệu. Ứng dụng cung cấp giao diện dòng lệnh (CLI) để quản lý nhân viên, phòng ban, chức vụ, chấm công và tính toán lương.

## 🛠️ Công nghệ sử dụng

* **Ngôn ngữ:** Python 3.14
* **Cơ sở dữ liệu:** MongoDB
* **Thư viện Python:**
    * `pymongo`: Để kết nối và thao tác với MongoDB.
    * `pandas`: Để hiển thị dữ liệu dạng bảng (DataFrame) trên CLI.
    * `python-dotenv`: Để quản lý biến môi trường (ví dụ: chuỗi kết nối MongoDB).

## 🚀 Tính năng chính

Ứng dụng được chia thành các module quản lý chính:

### 1. Quản lý Nhân viên
* Thêm nhân viên mới.
* Hiển thị danh sách nhân viên.
* Tìm kiếm nhân viên theo ID hoặc tên.
* Cập nhật thông tin nhân viên.
* Xóa (hoặc thay đổi trạng thái) nhân viên.

### 2. Quản lý Phòng ban
* Thêm phòng ban mới.
* Hiển thị danh sách phòng ban.
* Thống kê số lượng nhân viên và thông tin Trưởng phòng theo từng phòng ban.

### 3. Quản lý Chức vụ
* Thêm chức vụ mới (có định nghĩa mức lương tối thiểu/tối đa).
* Hiển thị danh sách chức vụ.

### 4. Chấm công
* **Check-in:** Ghi nhận giờ vào làm việc tự động (lấy giờ hệ thống).
* **Check-out:** Ghi nhận giờ kết thúc, tự động tính toán số phút đi muộn (`late_minutes`) và về sớm (`leave_minutes`) dựa trên ca mặc định (`08:00 - 17:00`).
* Xem lịch sử chấm công của từng nhân viên.

### 5. Quản lý Lương
* **Tính lương tháng:**
    * Truy xuất **lương cơ bản** (từ chức vụ) và **ngày công/phút muộn** (từ chấm công).
    * Cho phép nhập thêm các yếu tố: giờ OT, thưởng, phụ cấp, KPI.
    * Áp dụng các **quy tắc tính lương** (phụ cấp, thưởng, OT multiplier) theo chức vụ.
    * Tính toán **Lương Gross**, **Khấu trừ** (BHXH, Công đoàn, Thuế TNCN, Phạt đi muộn), và **Lương Net**.
* Lưu bảng lương vào cơ sở dữ liệu.
* Xem bảng lương chi tiết của nhân viên.

## ⚙️ Cấu trúc dự án

```
├── src/ # Thư mục chứa mã nguồn chính
│ ├── database.py # Thiết lập kết nối MongoDB 
│ ├── main.py # Điểm khởi chạy ứng dụng 
│ ├── models.py # Định nghĩa các lớp đối tượng và Hằng số tính lương 
│ ├── services.py # Các lớp service chứa logic thao tác với DB (CRUD) 
│ └── ui.py # Quản lý giao diện dòng lệnh (CLI) và các menu chức năng 
├── .gitattributes # Cấu hình Git attributes 
└── .gitignore # Danh sách file/thư mục bỏ qua
```

## 📋 Hướng dẫn cài đặt và chạy

### 1. Cài đặt MongoDB

Đảm bảo bạn đã có **MongoDB** server đang chạy (local hoặc Atlas).

### 2. Thiết lập biến môi trường

Tạo file `.env` trong thư mục gốc của dự án và điền thông tin kết nối MongoDB (thay thế giá trị `<...>` bằng thông tin thực tế):

```dotenv
# .env file
MONGO_URI="mongodb+srv://<user>:<password>@<cluster-url>/..."
DB_NAME="HRM_Database"
```

Lưu ý: Thêm file .env vào file .gitignore để tránh bị đẩy lên GitHub.

### 3. Cài đặt thư viện Python

Sử dụng pip để cài đặt các thư viện cần thiết:

```
pip install pymongo pandas python-dotenv
```

### 4. Chạy ứng dụng
Chạy file `main.py` nằm trong thư mục `src/` từ terminal:

```
python src/main.py
```
