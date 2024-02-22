import cv2
import os
import face_recognition
import datetime
import requests
def send_to_firebase(name, date):
    FIREBASE_URL = 'https://attendanceapp-e4818-default-rtdb.firebaseio.com/'
    data = {'name': name, 'date': date}
    response = requests.post(f'{FIREBASE_URL}/attendance.json', json=data)

    if response.status_code == 200:
        print(f"Data sent to Firebase - Date: {date}, Name: {name}")
    else:
        print(f"Failed to send data to Firebase. Status code: {response.status_code}")

def capture_and_recognize_person():
    
    cap = cv2.VideoCapture(1)
    ret, frame = cap.read()
    cap.release()
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    image_path = os.path.join(desktop_path, "captured_image.jpg")
    cv2.imwrite(image_path, frame)
    print(f"Image saved to: {image_path}")
    image = face_recognition.load_image_file(image_path)
    face_locations = face_recognition.face_locations(image)

    if not face_locations:
        print("No faces found in the image.")
        return
    
    dataset_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Dataset")

    known_face_encodings = []
    known_face_names = []

    for root, dirs, files in os.walk(dataset_folder):
        for person_image in files:
            person_image_path = os.path.join(root, person_image)
            person_name = os.path.basename(os.path.normpath(root))  

            person_face = face_recognition.load_image_file(person_image_path)
            person_face_encoding = face_recognition.face_encodings(person_face)[0]

            known_face_encodings.append(person_face_encoding)
            known_face_names.append(person_name)

    
    face_encodings = face_recognition.face_encodings(image, face_locations)

    for face_encoding in face_encodings:
        
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

            now = datetime.datetime.now()
            today_date = now.strftime("%Y-%m-%d")

            send_to_firebase(name, today_date)
           
    

if __name__ == "__main__":
    capture_and_recognize_person()
