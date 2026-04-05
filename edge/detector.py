import cv2

class FaceDetector:
    def __init__(self):
        self.model = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )

    def detect(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return self.model.detectMultiScale(gray, 1.3, 5)