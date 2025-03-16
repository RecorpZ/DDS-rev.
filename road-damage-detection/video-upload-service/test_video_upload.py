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

def test_upload_video_success(client, cleanup_uploads):
    test_file_path = "test_video.mp4"
    with open(test_file_path, "wb") as f:
        f.write(b"fake video data")

    # Отправляем POST-запрос
    response = client.post("/upload", json={"file_path": test_file_path})

    # Проверяем ответ
    assert response.status_code == 200
    assert response.json() == {
        "video_id": "test_video.mp4",
        "message": "File uploaded successfully"
    }

    # Проверяем, что файл скопирован в папку uploads
    assert os.path.exists("uploads/test_video.mp4")

    # Удаляем временный файл
    os.remove(test_file_path)

def test_upload_video_file_not_found(client, cleanup_uploads):
    # Отправляем POST-запрос с несуществующим файлом
    response = client.post("/upload", json={"file_path": "non_existent_file.mp4"})

    # Проверяем ответ
    assert response.status_code == 400
    assert response.json() == {"detail": "File not found"}

# Тесты для эндпоинта /list
def test_list_uploaded_videos_empty(client, cleanup_uploads):
    # Отправляем GET-запрос, когда папка uploads пуста
    response = client.get("/list")

    # Проверяем ответ
    assert response.status_code == 200
    assert response.json() == {"files": []}

def test_list_uploaded_videos_with_files(client, cleanup_uploads):
    # Создаем временные файлы в папке uploads
    with open("uploads/test_video1.mp4", "wb") as f:
        f.write(b"fake video data 1")
    with open("uploads/test_video2.mp4", "wb") as f:
        f.write(b"fake video data 2")

    # Отправляем GET-запрос
    response = client.get("/list")

    # Проверяем ответ
    assert response.status_code == 200
    assert response.json() == {"files": ["test_video1.mp4", "test_video2.mp4"]}