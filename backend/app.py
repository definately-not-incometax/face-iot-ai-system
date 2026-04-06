# 🔥 VERY IMPORTANT: ADD THIS FIRST
import sys
sys.path.append("/mnt/usb/python-packages")

from flask import Flask, request, jsonify, Response
from flask_socketio import SocketIO
import json
import os
import cv2
from datetime import datetime

# -------------------------------
# INIT APP
# -------------------------------
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

LOGS = []
DB_PATH = "../db/embeddings.json"

# -------------------------------
# LOAD DATABASE SAFELY
# -------------------------------
def load_db():
    if not os.path.exists(DB_PATH):
        return {}
    try:
        with open(DB_PATH, "r") as f:
            return json.load(f)
    except:
        return {}

def save_db(db):
    with open(DB_PATH, "w") as f:
        json.dump(db, f)

# -------------------------------
# ROUTES
# -------------------------------

@app.route("/")
def home():
    return "🔥 Face IoT Backend Running"

@app.route("/logs")
def get_logs():
    return jsonify(LOGS)

@app.route("/event", methods=["POST"])
def receive_event():
    data = request.json

    event = {
        "name": data.get("name", "Unknown"),
        "time": datetime.now().strftime("%H:%M:%S")
    }

    LOGS.append(event)

    # Emit to frontend (real-time)
    socketio.emit("new_event", event)

    return jsonify({"status": "ok"})

@app.route("/enroll", methods=["POST"])
def enroll():
    name = request.form["name"]
    embedding = json.loads(request.form["embedding"])

    db = load_db()
    db[name] = embedding
    save_db(db)

    return jsonify({"status": "saved"})

# -------------------------------
# VIDEO STREAM (IMPORTANT 🔥)
# -------------------------------
camera = cv2.VideoCapture(0)

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break

        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/video')
def video():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# -------------------------------
# MAIN
# -------------------------------
if __name__ == "__main__":
    print("🚀 Starting Backend Server...")
    socketio.run(app, host="0.0.0.0", port=5000)