import cv2 as cv
import face_recognition
import numpy as np

def recognize_face(frame, know_embeddings, tolerance = 0.6):
    '''
    Read frame from my webcame
    -> Resize image become smaller -> get increase speed of calculate 
    '''
    # preprocessing 
    small_frame = cv.resize(frame, (0,0), fx = 0.5, fy = 0.5) # resize samll a half
    rgb_frame = cv.cvtColor(small_frame, cv.COLOR_BGR2RGB) # convert image to RGB image (because function recognition using RGB color image)
   
    # location and encoding
    face_locations = face_recognition.face_locations(rgb_frame) # return top, right, botton, left
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations) # encoding (location of frame) to compare with encodings orginal file  (NOTES: Maybe have more faces in frame)
    
    results = []
    
    # Travesal each face in frame
    for current_encoding, current_location in zip(face_encodings, face_locations):
        # Get embedding in file .pkl 
        list_known_embeddings = []
        for item in know_embeddings:
            list_known_embeddings.append(item["embedding"])
        
        # calculate distance 
        distances = face_recognition.face_distance(list_known_embeddings,current_encoding)
        smallest_distance = np.min(distances)
        index_suitable = np.argmin(distances)
        
        # compare
        if smallest_distance < tolerance:
            detected_name = know_embeddings[index_suitable]['name']
            confidence = round ((1 - smallest_distance)*100,2)
        else:
            detected_name = "Unknown"
            
        # restore image size
        top, right, bottom, left = [int(x * 2) for x in current_location]
        
        cv.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv.FILLED)
        cv.putText(frame, f"{detected_name} ({confidence}%)", (left + 6, bottom - 6), cv.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

        results.append({
            "name":detected_name,
            "location":(top, right, bottom, left),
            "distance": float(smallest_distance)
        })
    return results

# import pickle
# with open("D:\STUDY\Face_Recognition_System\data\embedding.pkl", "rb") as f:
#     known_embeddings = pickle.load(f)

# cap = cv.VideoCapture(1)

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break

#     results = recognize_face(frame, known_embeddings)

#     cv.imshow("Face Recognition", frame)
#     if cv.waitKey(1) & 0xFF == 27:  # ESC
#         break

# cap.release()
# cv.destroyAllWindows()