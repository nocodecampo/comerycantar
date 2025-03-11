# config.py
import os

class Config:
    # Clave secreta para la sesión de Flask
    SECRET_KEY = os.environ.get('SECRET_KEY', 'clave_secreta_por_defecto')

    # Datos de conexión a la base de datos
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_USER = os.environ.get('DB_USER', 'root')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
    DB_NAME = os.environ.get('DB_NAME', 'reservas_restaurantes')