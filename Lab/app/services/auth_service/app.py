from flask import Flask, jsonify, request
import httpx
import asyncio

app = Flask(__name__)

# URL для User Service
USER_SERVICE_URL = "http://user_service:5000/users"

# Асинхронная функция для проверки пользователя
async def check_user(username, password):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{USER_SERVICE_URL}?username={username}")
            if response.status_code == 200:
                user = response.json()
                if user and user.get('password') == password:
                    return {"status": "success", "token": "fake_token"}
            return {"status": "failure", "message": "Invalid credentials"}
    except httpx.RequestError as e:
        return {"status": "error", "message": str(e)}

# Синхронный эндпоинт, который вызывает асинхронную функцию
@app.route('/auth', methods=['POST'])
def auth():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Запуск асинхронной функции в синхронном контексте
    result = asyncio.run(check_user(username, password))

    # Возврат результата
    if result.get("status") == "success":
        return jsonify(result)
    else:
        return jsonify(result), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)