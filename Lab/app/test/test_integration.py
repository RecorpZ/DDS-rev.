import requests

# Базовые URL сервисов
USER_SERVICE_URL = "http://user_service:5000"
AUTH_SERVICE_URL = "http://auth_service:5001"

def test_user_service():
    # Проверка получения списка пользователей
    response = requests.get(f"{USER_SERVICE_URL}/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_auth_service():
    # Проверка аутентификации
    response = requests.post(
        f"{AUTH_SERVICE_URL}/auth",
        json={"username": "admin", "password": "password"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_integration():
    # Проверка взаимодействия сервисов
    # 1. Аутентификация
    auth_response = requests.post(
        f"{AUTH_SERVICE_URL}/auth",
        json={"username": "admin", "password": "password"}
    )
    assert auth_response.status_code == 200
    assert auth_response.json()["status"] == "success"

    # 2. Получение списка пользователей
    user_response = requests.get(f"{USER_SERVICE_URL}/users")
    assert user_response.status_code == 200
    assert isinstance(user_response.json(), list)
