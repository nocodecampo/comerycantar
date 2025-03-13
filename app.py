from flask import Flask,render_template,request,redirect,url_for,session, flash
from werkzeug.security import check_password_hash,generate_password_hash
import pymysql
import db




app = Flask(__name__)
app.secret_key="123456"


@app.route('/')
def home():
    return render_template("home/home.html")

# -------------------------------
# 🔹 CLIENTE
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
                    return redirect(url_for('reservas'))  # Redirigir a reservas cliente
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

# -------------------------------
# 🔹 RESTAURANTE
# -------------------------------

#login restaurante
@app.route('/login-restaurante', methods=['GET', 'POST'])
def loginRestaurante():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conexion = db.get_connection()
        try:
            with conexion.cursor() as cursor:
                consulta = "SELECT * FROM restaurantes WHERE email = %s"
                cursor.execute(consulta, (email,))
                restaurante = cursor.fetchone()
                
                if restaurante and check_password_hash(restaurante['password_hash'], password):
                    session['restaurante_id'] = restaurante['restaurante_id']
                    session['email'] = restaurante['email']
                    return redirect(url_for('area_restaurante'))  # Redirigir a dashboard restaurante
                else:
                    flash("Usuario o contraseña incorrectos", "error")
                    
                    
                 
        
        finally:
            conexion.close()

    return render_template("login/login-restaurante.html") 

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

# EDITS DIEGO ----------------------------------------------

# Ver las reservas del cliente
@app.route('/area-cliente',methods=['GET'])
def reservas():
    if "cliente_id" not in session:
        return redirect(url_for('loginCliente'))
    conexion = db.get_connection()
    try:
        with conexion.cursor() as cursor:
            consulta = """
                SELECT r.reserva_id, rest.nombre AS restaurante_nombre, r.fecha, h.hora, r.num_personas, er.estado_nombre AS estado
                FROM reservas r
                JOIN restaurantes rest ON r.restaurante_id = rest.restaurante_id
                JOIN horarios h ON r.horario_id = h.horario_id
                JOIN estados_reserva er ON r.estado_id = er.estado_id
                WHERE r.cliente_id = %s
                ORDER BY r.fecha DESC, r.horario_id DESC
            """
            cursor.execute(consulta, (session["cliente_id"],))
            reservas = cursor.fetchall()
    finally:
        conexion.close()
    
    return render_template("area-privada/area-cliente.html", reservas=reservas)

# Ruta para cancelar reservas de cliente
@app.route('/cancelar-reserva/<int:reserva_id>', methods=['POST'])
def cancelar_reserva(reserva_id):
    if "cliente_id" not in session:
        return redirect(url_for('loginCliente'))
    
    conexion = db.get_connection()
    try:
        with conexion.cursor() as cursor:
            consulta = "UPDATE reservas SET estado_id = (SELECT estado_id FROM estados_reserva WHERE estado_nombre = 'cancelada') WHERE reserva_id = %s AND cliente_id = %s"
            cursor.execute(consulta, (reserva_id, session["cliente_id"]))
            conexion.commit()
            flash("Reserva cancelada con éxito.", "success")
    finally:
        conexion.close()
    
    return redirect(url_for('reservas'))

# ✅ Ruta para el área del restaurante
@app.route('/area-restaurante')
def area_restaurante():
       
    if "restaurante_id" not in session:
        return redirect(url_for('loginRestaurante'))      

    conexion = db.get_connection()
    try:
        with conexion.cursor() as cursor:
            # Obtener todas las mesas del restaurante
            consulta_mesas = "SELECT mesa_id, capacidad FROM mesas WHERE restaurante_id = %s"
            cursor.execute(consulta_mesas, (session["restaurante_id"],))
            mesas = cursor.fetchall()

            # Obtener todas las franjas horarias
            consulta_horarios = "SELECT horario_id, hora FROM horarios ORDER BY hora"
            cursor.execute(consulta_horarios)
            horarios = cursor.fetchall()

            # Obtener reservas activas del restaurante
            consulta_reservas = """
                SELECT r.reserva_id, r.mesa_id, r.horario_id, c.nombre AS cliente_nombre
                FROM reservas r
                JOIN clientes c ON r.cliente_id = c.cliente_id
                WHERE r.restaurante_id = %s AND r.estado_id = (SELECT estado_id FROM estados_reserva WHERE estado_nombre = 'activa')
            """
            cursor.execute(consulta_reservas, (session["restaurante_id"],))
            reservas_lista = cursor.fetchall()

            # Convertir reservas en un diccionario para acceso rápido
            reservas = {(reserva["mesa_id"], reserva["horario_id"]): reserva for reserva in reservas_lista}

    finally:
        conexion.close()

    return render_template("area-privada/area-restaurante.html", mesas=mesas, horarios=horarios, reservas=reservas)

# ✅ Confirmar una reserva
@app.route('/confirmar-reserva/<int:reserva_id>', methods=['POST'])
def confirmar_reserva(reserva_id):
    if "restaurante_id" not in session:
        return redirect(url_for('loginRestaurante'))
    
    conexion = db.get_connection()
    try:
        with conexion.cursor() as cursor:
            consulta = """
                UPDATE reservas 
                SET estado_id = (SELECT estado_id FROM estados_reserva WHERE estado_nombre = 'pasada') 
                WHERE reserva_id = %s AND restaurante_id = %s
            """
            cursor.execute(consulta, (reserva_id, session["restaurante_id"]))
            conexion.commit()
            flash("Reserva confirmada.", "success")
    finally:
        conexion.close()

    return redirect(url_for('area_restaurante'))

# ✅ Cancelar una reserva (desde el restaurante)
@app.route('/cancelar-reserva-restaurante/<int:reserva_id>', methods=['POST'])
def cancelar_reserva_restaurante(reserva_id):
    if "restaurante_id" not in session:
        return redirect(url_for('loginRestaurante'))

    conexion = db.get_connection()
    try:
        with conexion.cursor() as cursor:
            # 🔹 Verificar si la reserva pertenece al restaurante antes de cancelarla
            consulta_verificar = "SELECT reserva_id FROM reservas WHERE reserva_id = %s AND restaurante_id = %s"
            cursor.execute(consulta_verificar, (reserva_id, session["restaurante_id"]))
            reserva = cursor.fetchone()

            if reserva:  # Solo se cancela si la reserva pertenece al restaurante
                consulta_cancelar = """
                    UPDATE reservas 
                    SET estado_id = (SELECT estado_id FROM estados_reserva WHERE estado_nombre = 'cancelada') 
                    WHERE reserva_id = %s
                """
                cursor.execute(consulta_cancelar, (reserva_id,))
                conexion.commit()
                flash("Reserva cancelada con éxito.", "warning")
            else:
                flash("No tienes permiso para cancelar esta reserva.", "danger")
    finally:
        conexion.close()

    return redirect(url_for('area_restaurante'))

# ✅ Agregar una nueva mesa
@app.route('/agregar-mesa', methods=['POST'])
def agregar_mesa():
    if "restaurante_id" not in session:
        return redirect(url_for('loginRestaurante'))

    try:
        capacidad = int(request.form["capacidad"])  # 🔹 Convertir a entero y validar

        if capacidad < 1:  # 🔹 Evitar números negativos o cero
            flash("El número de comensales debe ser mayor a 0.", "danger")
            return redirect(url_for('area_restaurante'))

        conexion = db.get_connection()
        try:
            with conexion.cursor() as cursor:
                consulta = "INSERT INTO mesas (restaurante_id, capacidad, estado) VALUES (%s, %s, 'disponible')"
                cursor.execute(consulta, (session["restaurante_id"], capacidad))
                conexion.commit()
                flash("Mesa agregada con éxito.", "success")
        finally:
            conexion.close()

    except ValueError:  # 🔹 Maneja errores si `capacidad` no es un número válido
        flash("Por favor, ingresa un número válido de comensales.", "danger")

    return redirect(url_for('area_restaurante'))


@app.route('/nueva-reserva', methods=['GET', 'POST'])
def nueva_reserva():
    if request.method == 'POST':
        # Recoge los datos del formulario
        fecha = request.form['fecha']
        horario_id = request.form['horario_id']
        num_personas = request.form['num_personas']
        restaurante_id = request.form['restaurante_id']
        cliente_id = session['cliente_id']  # Asumiendo que el cliente está logueado y su ID está en la sesión

        # TODO: Validar los datos recibidos del formulario (puedes agregar más validaciones aquí)

        try:
            # Conexión a la base de datos
            connection = db.get_connection()
            cursor = connection.cursor()

            # Lógica para encontrar una mesa disponible
            query_mesas_disponibles = """
                SELECT mesa_id FROM mesas 
                WHERE restaurante_id = %s AND capacidad >= %s AND estado = 'disponible'
                AND mesa_id NOT IN (
                    SELECT mesa_id FROM reservas
                    WHERE fecha = %s AND horario_id = %s
                )
                LIMIT 1
            """
            cursor.execute(query_mesas_disponibles, (restaurante_id, num_personas, fecha, horario_id))
            mesa_disponible = cursor.fetchall()

            if mesa_disponible:
                mesa_id = mesa_disponible[0]

                # Crea la reserva en la base de datos
                query_insert_reserva = """
                    INSERT INTO reservas (cliente_id, restaurante_id, mesa_id, estado_id, fecha, horario_id, num_personas)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                estado_id = 1  # 'activa'
                cursor.execute(query_insert_reserva, (cliente_id, restaurante_id, mesa_id["mesa_id"], estado_id, fecha, horario_id, num_personas))
                connection.commit()

                # TODO: Actualizar el estado de la mesa a 'ocupada' si es necesario

                # Redirige a una página de confirmación (puedes mostrar un mensaje o redirigir)
                return redirect(url_for('reservas'))  # O redirigir a una página específica de confirmación
            else:
                # Si no hay mesas disponibles, muestra un mensaje de error
                return render_template("reservas/nueva-reserva.html", error="No hay mesas disponibles para la fecha, hora y número de personas seleccionados.", restaurantes=restaurantes, horarios=horarios)

        except pymysql.Error as e:
            print("Error al realizar la reserva:", e)
            return "Error al realizar la reserva. Por favor, inténtelo de nuevo más tarde."
        finally:
            if connection:
                cursor.close()
                connection.close()

    # Si es una petición GET, muestra el formulario de reserva con los restaurantes y horarios
    try:
        connection = db.get_connection()
        cursor = connection.cursor()

        # Obtener los restaurantes
        cursor.execute("SELECT restaurante_id, nombre FROM restaurantes")
        restaurantes = cursor.fetchall()

        # Obtener los horarios
        cursor.execute("SELECT horario_id, hora FROM horarios")
        horarios = cursor.fetchall()

        cursor.close()
        connection.close()

        return render_template("reservas/nueva-reserva.html", restaurantes=restaurantes, horarios=horarios)

    except pymysql.Error as e:
        print("Error al obtener los restaurantes o horarios:", e)
        return "Error al cargar los datos necesarios para la reserva."



if __name__ == '__main__':
    app.run(debug=True, port=80)
