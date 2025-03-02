from flask import Flask, jsonify, request, abort
import sqlite3

app = Flask(__name__)

# Подключение к базе данных
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # Возвращает строки как словари
    return conn

@app.route('/users', methods=['GET'])
def get_users():
    username = request.args.get('username')
    conn = get_db_connection()
    cursor = conn.cursor()

    if username:
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()
        if user:
            return jsonify(dict(user))
        abort(404)
    else:
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()
        conn.close()
        return jsonify([dict(user) for user in users])

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    if not username or not password or not email:
        abort(400, description="Missing required fields")

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            'INSERT INTO users (username, password, email) VALUES (?, ?, ?)',
            (username, password, email)
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return jsonify({"id": user_id, "username": username, "email": email}), 201
    except sqlite3.IntegrityError:
        conn.close()
        abort(409, description="Username already exists")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)