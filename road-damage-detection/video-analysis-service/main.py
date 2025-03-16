from fastapi import FastAPI, UploadFile, File
import os
import cv2
import torch

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

model = torch.hub.load('ultralytics/yolov8', 'yolov8n')

@app.post("/analyze")
async def analyze_video(file: UploadFile = File(...)):

    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as f:
        f.write(await file.read())


    detections = []
    cap = cv2.VideoCapture(file_location)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)
        detections.append(results)

    cap.release()


    damage_count = sum(len(r.boxes) for r in detections)
    return {"filename": file.filename, "damage_count": damage_count}


@app.get("/list")
async def list_uploaded_videos():

    files = os.listdir(UPLOAD_DIR)
    return {"files": files}