from flask import Flask, render_template, Response, request, redirect, url_for, flash
import cv2 as cv
import pickle 
import os
import time
from recognize_faces import recognize_face
from database_utils import init_database, log_attendance, get_attendance, get_attendance_by_date, get_people
from werkzeug.utils import secure_filename # Function to project file when update file (advoid error security)

# Init app Flask with templates 
app = Flask(__name__, template_folder="D:\STUDY\Face_Recognition_System\\templates") 
app.secret_key = "supersecretkey"
app.config["UPLOAD_FOLDER"] = "D:\\STUDY\\Face_Recognition_System\\static\\uploads" # store new images when updates 

# load embeddings from embedding.pkl 
with open("D:\STUDY\Face_Recognition_System\data\embedding.pkl", "rb") as f:
    known_embeddings = pickle.load(f)
    
# init database
database_path = "D:\STUDY\Face_Recognition_System\database\\attendance.db"
init_database(database_path)

cap = cv.VideoCapture(1) 

last_logged = {}   # dicitionary to save time of attendance of each person (avoid repeat)

def gen_frames():
    global last_logged 
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        results = recognize_face(frame, known_embeddings) # detect all faces in each frame of webcam

        for result in results :
            name = result["name"]
            top, right, bottom, left = result["location"] 
            
            #display
            cv.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv.putText(frame, name, (left, top - 10), cv.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            
            # Mark attendance if person has logged within 10s 
            current_time = time.time()
            if name != "Unknown":
                if name not in last_logged or current_time - last_logged[name] > 10:
                    log_attendance(name, database_path)
                    last_logged[name] = current_time
                    print(f"[INFO] {name} đã điểm danh lúc {time.strftime('%H:%M:%S')}")
            
            # encoding frame from jpg to convert -> html 
            ret, buffer = cv.imencode(".jpg", frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route("/")
def index():
    return render_template("index.html") # just file name

# open webcam 
@app.route("/video_feed")
def video_feed():
    return Response(gen_frames(), mimetype = "multipart/x-mixed-replace; boundary=frame")

@app.route("/attendance")
def attendance():
    records = get_attendance(database_path)
    people = get_people(database_path)
    return render_template("attendance.html", records=records, people=people)

@app.route("/add_person", methods=["GET", "POST"])
def add_person():
    if request.method == "POST":
        name = request.form["name"]
        files = request.files.getlist("images")
        if not name or not files:
            flash("Vui lòng nhập tên và chọn ít nhất một ảnh.")
            return redirect(url_for("add_person"))

        person_dir = os.path.join("D:\\STUDY\\Face_Recognition_System\\data\\images", secure_filename(name))
        os.makedirs(person_dir, exist_ok=True)

        for file in files:
            if file:
                filename = secure_filename(file.filename)
                file.save(os.path.join(person_dir, filename))

        from embedding_face import extract_embedding
        extract_embedding()  # Re-generate embeddings

        global known_embeddings
        with open("D:\STUDY\Face_Recognition_System\data\embedding.pkl", "rb") as f:
            known_embeddings = pickle.load(f)

        flash(f"Đã thêm {name} thành công!")
        return redirect(url_for("index"))

    return render_template("add_person.html")  


@app.route("/delete_person/<name>")
def delete_person(name):
    import shutil
    person_dir = os.path.join("D:\\STUDY\\Face_Recognition_System\\data\\images", name)
    if os.path.exists(person_dir):
        shutil.rmtree(person_dir)
        from src.embedding_face import extract_embedding
        extract_embedding()

        global known_embeddings
        with open("D:\\STUDY\\Face_Recognition_System\\data\\embedding.pkl", "rb") as f:
            known_embeddings = pickle.load(f)

        # Xóa khỏi last_logged khi xóa người
        global last_logged
        if name in last_logged:
            del last_logged[name]

        flash(f"Đã xóa {name} thành công!")
    else:
        flash(f"Không tìm thấy {name}!")
    return redirect(url_for("attendance"))

if __name__ == "__main__":
    try:
        app.run(debug=True)
    finally:
        cap.release()