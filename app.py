from flask import Flask,render_template,request,redirect,url_for,session, flash
from werkzeug.security import check_password_hash,generate_password_hash
import pymysql
import db




app = Flask(__name__)
app.secret_key="123456"

# -------------------------------
# 🔹 LOGIN CLIENTE
# -------------------------------
@app.route('/login-cliente', methods=['GET', 'POST'])
def loginCliente():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conexion = db.get_connection()
        try:
            with conexion.cursor() as cursor:
                consulta = "SELECT * FROM clientes WHERE email = %s "
                cursor.execute(consulta, (email,))
                cliente = cursor.fetchone()

                if cliente and check_password_hash(cliente['password_hash'], password):
                    session['cliente_id'] = cliente['cliente_id']
                    session['email'] = cliente['email']
                    return redirect(url_for('dashboard_cliente'))  # Redirigir a dashboard cliente
                else:
                    flash("Usuario o contraseña incorrectos", "danger")
        finally:
            conexion.close()

    return render_template("login/login-cliente.html")

@app.route('/logout')
def logout():
    # Eliminar los datos de la sesión
    session.clear()  # Esto elimina todas las variables de sesión

    # Redirigir al login o a la página de inicio
    return redirect(url_for('loginCliente'))  # redirigir a  página de eleccion , de momento loginCliente , despues?->'home'
  

@app.route('/dashboard-cliente')
def dashboard_cliente():
    if 'cliente_id' in session:
        return render_template("reservas/nueva-reserva.html")
    else:
        return redirect(url_for('loginCliente'))

    
@app.route('/registro-cliente', methods=['GET', 'POST'])
def registroCliente():
    if request.method == 'POST':
        # Recoger los datos del formulario
        nombre = request.form['nombre']
        email = request.form['email']
        telefono = request.form['telefono']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        # Conexión a la base de datos
        connection = db.get_connection()
        with connection.cursor() as cursor:
            # Insertar los datos en la tabla correspondiente
            sql = "INSERT INTO clientes (nombre, email, telefono, password_hash) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (nombre, email, telefono, hashed_password))
            connection.commit()
        connection.close()

        # Redirigir a una página de éxito o login
        return redirect(url_for('loginCliente'))

    return render_template("registro/registro-cliente.html")


# Ruta de registro de restaurante (GET y POST)
@app.route('/registro-restaurante', methods=['GET', 'POST'])
def registroRestaurante():
    if request.method == 'POST':
        # Recoger los datos del formulario
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        ciudad = request.form['ciudad']
        telefono = request.form['telefono']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        # Conexión a la base de datos
        connection = db.get_connection()
        with connection.cursor() as cursor:
            # Insertar los datos en la tabla correspondiente
            sql = "INSERT INTO restaurantes (nombre, direccion, ciudad, telefono, email, password_hash) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (nombre, direccion, ciudad, telefono, email, hashed_password))
            connection.commit()
        connection.close()

        # Redirigir a una página de éxito o login
        return redirect(url_for('loginRestaurante'))

    return render_template("registro/registro-restaurante.html")


if __name__ == '__main__':
    app.run(debug=True, port=80)
