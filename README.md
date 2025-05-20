# Mô tả dự án: Hệ thống Điểm danh bằng Nhận diện Khuôn mặt
Hệ thống sử dụng webcam để nhận diện khuôn mặt theo thời gian thực, ghi lại thông tin điểm danh (tên người, thời gian) vào cơ sở dữ liệu SQLite, và cung cấp giao diện web để quản lý và theo dõi dữ liệu

# Tính năng:
Nhận diện khuôn mặt theo thời gian thực qua webcam
Lưu thông tin điểm danh vào cơ sở dữ liệu SQLite
Giao diện web để xem lịch sử điểm danh, thêm/xóa người
Công cụ: Flask, OpenCV, face_recognition, SQLite, HTML/CSS

# Requirement
Python 3.8+
Thư viện: flask, opencv-python, face_recognition, numpy, pillow
Cài đặt cmake và dlib để sử dụng face_recognition

# Setup 
## 1. Clone repo
``` bash  git clone https://github.com/mDoanzz43/Face_Recognition_System.git '''

## 2. Setup virtual environment 
'''
python -m venv venv
.\venv\Scripts\activate  # Windows
'''

## 3. Library
'''
pip install -r requirement.txt
'''

## 4. Run 
'''
python app.py
'''

## 5. Truy cập địa chỉ localhost

# Sử dụng
Thêm ảnh vào data/images/[tên_người]/ để huấn luyện.
Truy cập giao diện web để xem điểm danh, thêm/xóa người.

## Fun Project
## Enjoy and chill~

