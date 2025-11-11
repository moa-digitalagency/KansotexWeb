import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SESSION_SECRET') or 'dev-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError("DATABASE_URL environment variable is not set. Please configure your database connection.")
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
    
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024
