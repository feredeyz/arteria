from secrets import token_hex
from datetime import timedelta
class Config:
    SECRET_KEY = '617545da60b6385f1ac80bfa4e58157c4c97a8b24223d9a977745012dd01926e835343ebca744cb82586'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data.db'
    JWT_COOKIE_SECURE = False
    JWT_TOKEN_LOCATION = ["cookies"]
    JWT_SECRET_KEY = token_hex(52)
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_COOKIE_SECURE = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=5)
    JWT_ACCESS_COOKIE_NAME = 'access_token_cookie'
    LOGIN_VIEW = "auth.login"