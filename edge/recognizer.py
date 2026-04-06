import insightface
import numpy as np
import json
import cv2

class FaceRecognizer:
    def __init__(self, db_path="../db/embeddings.json"):
        self.model = insightface.app.FaceAnalysis()
        self.model.prepare(ctx_id=0)

        with open(db_path, "r") as f:
            self.db = json.load(f)

    def recognize(self, frame, bbox):
        x, y, w, h = bbox
        face_img = frame[y:y+h, x:x+w]

        faces = self.model.get(face_img)

        if len(faces) == 0:
            return "Unknown"

        emb = faces[0].embedding

        best_match = "Unknown"
        min_dist = float("inf")

        for name, known_emb in self.db.items():
            dist = np.linalg.norm(np.array(known_emb) - np.array(emb))
            if dist < min_dist and dist < 1.2:
                min_dist = dist
                best_match = name

        return best_match