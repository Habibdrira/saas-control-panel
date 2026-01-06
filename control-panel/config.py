import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key')
    MICROBLOG_API_URL = os.environ.get('MICROBLOG_API_URL', 'http://localhost')
    MICROBLOG_API_KEY = os.environ.get('MICROBLOG_API_KEY', 'changeme')

# ===== Simple Admin Auth =====
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"
SECRET_KEY = "control-panel-secret"
