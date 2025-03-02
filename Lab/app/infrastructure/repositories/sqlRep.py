from app.domain.user import User
from app.infrastructure.database import Database

class MySQLUserRepository:
    def __init__(self, db):
        self.db = db

    def find_all(self):
        query = "SELECT id, name, email, password FROM users"
        rows = self.db.execute_query(query)
        return [User(id=row[0], name=row[1], email=row[2], password=row[3]) for row in rows]

    def find_by_id(self, user_id):
        query = "SELECT id, name, email, password FROM users WHERE id = %s"
        row = self.db.execute_query(query, (user_id,), fetch_one=True)
        if row:
            return User(id=row[0], name=row[1], email=row[2], password=row[3])
        return None

    def save(self, user):
        if user.id:
            query = "UPDATE users SET name = %s, email = %s, password = %s WHERE id = %s"