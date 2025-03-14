import os

class Config:
    # Clave secreta para la sesión de Flask
    SECRET_KEY = os.environ.get('SECRET_KEY', 'clave_secreta_por_defecto')

    # Datos de conexión a la base de datos
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_USER = os.environ.get('DB_USER', 'root')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
    DB_NAME = os.environ.get('DB_NAME', 'reservas_restaurantes')

    # Configuración del servidor de correo (Ejemplo con Gmail)
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME", "itcode1992@gmail.com")  # Cambia esto
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", "rftk qoak aijl tkuw")  # Usa una contraseña segura (o App Password)
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER", "itcode1992@gmail.com")  # Usa tu correo aquí

