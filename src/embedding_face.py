import face_recognition
import pickle
import os

data_dir =  "D:\STUDY\Face_Recognition_System\data\images"
output_file = "D:\STUDY\Face_Recognition_System\data\embedding.pkl"

def extract_embedding():
    '''
    Hàm trích xuất vector đặc trưng khuôn mặt
    input: Images 
    Output: embeddings file
    ''' 
    embedding = []
    
    # Travesal each person 
    for person_name in os.listdir(data_dir):
        person_dir = os.path.join(data_dir, person_name)
       
        if not os.path.isdir(person_dir):
            continue
        # print(person_dir)
        
        for image_name in os.listdir(person_dir):
            image_path = os.path.join(person_dir, image_name)
            # print(image_path)
        
            #  Load image
            image = face_recognition.load_image_file(image_path)
            # Encoder -> vector -> emdedding
            encoding = face_recognition.face_encodings(image)
            
            if encoding:
                embedding.append({
                    "name": person_name,
                    "embedding": encoding[0]  
                })  
        
        # Save embeddings -> pickle
        with open(output_file, 'wb') as f:
            pickle.dump(embedding, f)
            
        print(f"Saved {len(embedding)} embeddings to {output_file}")


if __name__ == "__main__":
    extract_embedding()