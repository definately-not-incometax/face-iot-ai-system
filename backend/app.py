from flask import Flask, request, jsonify
from flask_socketio import SocketIO
import json
import os

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

LOGS = []
DB_PATH = "../db/embeddings.json"

@app.route("/logs")
def get_logs():
    return jsonify(LOGS)

@app.route("/enroll", methods=["POST"])
def enroll():
    name = request.form["name"]
    embedding = json.loads(request.form["embedding"])

    if os.path.exists(DB_PATH):
        with open(DB_PATH, "r") as f:
            db = json.load(f)
    else:
        db = {}

    db[name] = embedding

    with open(DB_PATH, "w") as f:
        json.dump(db, f)

    return {"status": "enrolled"}

@app.route("/event", methods=["POST"])
def event():
    data = request.json
    LOGS.append(data)
    socketio.emit("new_event", data)
    return {"status": "ok"}

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)