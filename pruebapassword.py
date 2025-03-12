from werkzeug.security import generate_password_hash, check_password_hash

# Genera un hash de prueba
password = "1234"
hashed_password = generate_password_hash(password)
print(f"Hash generado: {hashed_password}")

# Verifica el hash con una contraseña de prueba
test_password = "mi_contraseña_segura"
if check_password_hash(hashed_password, password):
    print("Contraseña correcta")
else:
    print("Contraseña incorrecta")
