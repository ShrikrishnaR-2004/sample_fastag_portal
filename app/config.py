import os
from dotenv import load_dotenv
load_dotenv()
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-dev-secret-key')
    _user = os.getenv('DB_USERNAME', 'root')
    _pw   = os.getenv('DB_PASSWORD', '')
    _host = os.getenv('DB_HOST', 'localhost')
    _port = os.getenv('DB_PORT', '3306')
    _db   = os.getenv('DB_NAME', 'fastag_portal')
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{_user}:{_pw}@{_host}:{_port}/{_db}"
        "?charset=utf8mb4"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_recycle": 280,
        "pool_pre_ping": True,
    }
    MAIL_SERVER        = os.getenv('MAIL_SERVER', 'localhost')
    MAIL_PORT          = int(os.getenv('MAIL_PORT', 1025))
    MAIL_USE_TLS       = os.getenv('MAIL_USE_TLS', 'False').lower() == 'true'
    MAIL_USE_SSL       = False
    MAIL_USERNAME      = os.getenv('MAIL_USERNAME') or None
    MAIL_PASSWORD      = os.getenv('MAIL_PASSWORD') or None
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@fastag.nhai.gov.in')
    OTP_DEMO_MODE     = os.getenv('OTP_DEMO_MODE', 'True').lower() == 'true'
    OTP_DEMO_CODE     = os.getenv('OTP_DEMO_CODE', '123456')
    OTP_EXPIRY_SECONDS = int(os.getenv('OTP_EXPIRY_SECONDS', 300))
    TWILIO_ACCOUNT_SID  = os.getenv('TWILIO_ACCOUNT_SID', '')
    TWILIO_AUTH_TOKEN   = os.getenv('TWILIO_AUTH_TOKEN', '')
    TWILIO_FROM_NUMBER  = os.getenv('TWILIO_FROM_NUMBER', '')
    LOGIN_VIEW      = 'main.login'
    REMEMBER_COOKIE_DURATION = 86400  
    RESET_TOKEN_EXPIRY_MINUTES = 30
    PASSWORD_HISTORY_LIMIT     = 3
    # Pepper for HMAC-SHA256 hashing of Aadhaar / PAN (never store plaintext)
    KYC_PEPPER = os.getenv('KYC_PEPPER', 'change-this-pepper-in-production')
class DevelopmentConfig(Config):
    DEBUG = True
class ProductionConfig(Config):
    DEBUG = False
    MAIL_USE_TLS = True
config = {
    'development': DevelopmentConfig,
    'production':  ProductionConfig,
    'default':     DevelopmentConfig,
}
