from fastapi import FastAPI, HTTPException
import shutil
import os

app = FastAPI()

UPLOAD_DIRECTORY = "uploads"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

@app.post("/upload")
async def upload_video(file_path: str):
    try:

        if not os.path.isfile(file_path):
            raise HTTPException(status_code=400, detail="File not found")

        filename = os.path.basename(file_path)
        destination_path = os.path.join(UPLOAD_DIRECTORY, filename)

        shutil.copy(file_path, destination_path)

        return {"video_id": filename, "message": "File uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/list")
async def list_uploaded_videos():
    try:
        files = os.listdir(UPLOAD_DIRECTORY)
        return {"files": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))