import os

class Config:
    SECRET_KEY = '799e571239fb6a25aa2de9766f0fb172a7bd1d2e598872ea'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///posts.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    confirm_deleted_rows = False
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = '587'
    MAIL_USE_TLS = '587'
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
    
 