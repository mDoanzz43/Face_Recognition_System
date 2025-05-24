# 🤖 Mô tả dự án: Hệ thống Điểm danh bằng Nhận diện Khuôn mặt
Hệ thống sử dụng webcam để nhận diện khuôn mặt theo thời gian thực, ghi lại thông tin điểm danh (tên người, thời gian) vào cơ sở dữ liệu SQLite, và cung cấp giao diện web để quản lý và theo dõi dữ liệu

# ✨Tính năng:
- Nhận diện khuôn mặt theo thời gian thực qua webcam
- Lưu thông tin điểm danh vào cơ sở dữ liệu SQLite
- Giao diện web để xem lịch sử điểm danh, thêm/xóa người
- Công cụ: Flask, OpenCV, face_recognition, SQLite, HTML/CSS

#🛠️ Requirement
- Python 3.8+
- Thư viện: flask, opencv-python, face_recognition, numpy, pillow
- Cài đặt cmake và dlib để sử dụng face_recognition

# 🚀Setup chương trình 
## 1. Clone repo
``` bash  git clone https://github.com/mDoanzz43/Face_Recognition_System.git ```

## 2. Setup virtual environment 
``` bash
python -m venv venv
.\venv\Scripts\activate  # Windows
```

## 3. Library
``` bash
pip install -r requirement.txt
```

## 4. Run 
``` bash
python app.py
```

## 5. Truy cập địa chỉ localhost được hiển thị khi chạy file app.py

# Sử dụng
Thêm ảnh vào data/images/[tên_người]/ để huấn luyện.
Truy cập giao diện web để xem điểm danh, thêm/xóa người.

#📊 Kết quả demo:
![image](https://github.com/user-attachments/assets/c983f020-692e-4a44-a68c-9749b94565cf) ![image](https://github.com/user-attachments/assets/778ad219-0087-4064-b208-6016530699d2)


# 📄Tìm hiểu chi tiết bằng cách xem file report.pdf 
## Enjoy and chill~

