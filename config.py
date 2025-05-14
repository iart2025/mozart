# config.py

import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'supersecretkey')  # Utilizando variável de ambiente
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///../instance/mozart.db')  # Para diferentes bancos, use variáveis de ambiente
    SQLALCHEMY_TRACK_MODIFICATIONS = False
