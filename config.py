import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Get the project directory
class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'library.db')}"  # Store inside project folder
    SQLALCHEMY_TRACK_MODIFICATIONS = False
