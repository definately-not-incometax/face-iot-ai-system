import requests
import cv2
from camera import Camera
from detector import FaceDetector
from recognizer import FaceRecognizer

SERVER_URL = "http://localhost:5000"

camera = Camera()
detector = FaceDetector()
recognizer = FaceRecognizer()

while True:
    frame = camera.get_frame()
    if frame is None:
        break

    faces = detector.detect(frame)

    for (x, y, w, h) in faces:
        face = frame[y:y+h, x:x+w]
        name = recognizer.recognize(frame, (x, y, w, h))

        requests.post(f"{SERVER_URL}/event", json={
            "name": name,
            "time": str(cv2.getTickCount())
        })

        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
        cv2.putText(frame, name, (x,y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

    cv2.imshow("Edge AI", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break