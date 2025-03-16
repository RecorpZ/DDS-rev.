import os
import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client

@pytest.fixture
def cleanup_uploads():
    upload_dir = "uploads"
    if os.path.exists(upload_dir):
        for file in os.listdir(upload_dir):
            file_path = os.path.join(upload_dir, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
    else:
        os.makedirs(upload_dir)

def test_analyze_video_success(client, cleanup_uploads):
    test_file_path = "test_video.mp4"
    with open(test_file_path, "wb") as f:
        f.write(b"fake video data")

    with open(test_file_path, "rb") as f:
        response = client.post("/analyze", files={"file": f})

    assert response.status_code == 200
    assert "filename" in response.json()
    assert "damage_count" in response.json()

    assert os.path.exists("uploads/test_video.mp4")

    os.remove(test_file_path)

def test_list_uploaded_videos_empty(client, cleanup_uploads):
    response = client.get("/list")

    assert response.status_code == 200
    assert response.json() == {"files": []}

def test_list_uploaded_videos_with_files(client, cleanup_uploads):
    with open("uploads/test_video1.mp4", "wb") as f:
        f.write(b"fake video data 1")
    with open("uploads/test_video2.mp4", "wb") as f:
        f.write(b"fake video data 2")

    response = client.get("/list")

    assert response.status_code == 200
    assert set(response.json()["files"]) == {"test_video1.mp4", "test_video2.mp4"}