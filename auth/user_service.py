from database.connection import SessionLocal
from database.models import User
import bcrypt

db = SessionLocal()

def create_user(username, name, password, role="viewer"):
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    user = User(username=username, name=name, password=hashed, role=role)
    db.add(user)
    db.commit()
    return user

def get_user(username):
    return db.query(User).filter(User.username == username).first()
