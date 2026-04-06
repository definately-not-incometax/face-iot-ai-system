import insightface
import json
import cv2

model = insightface.app.FaceAnalysis()
model.prepare(ctx_id=0)

name = "YourName"
img_path = "../faces/yourname.jpg"

img = cv2.imread(img_path)
faces = model.get(img)

if len(faces) == 0:
    print("No face found!")
    exit()

embedding = faces[0].embedding.tolist()

with open("../db/embeddings.json", "r") as f:
    db = json.load(f)

db[name] = embedding

with open("../db/embeddings.json", "w") as f:
    json.dump(db, f)

print("Face enrolled successfully!")