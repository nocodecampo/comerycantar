from flask import Flask,render_template,request,redirect,url_for,session, flash
from werkzeug.security import check_password_hash
import pymysql
import db




app = Flask(__name__)
app.secret_key="123456"
# Conexión a la base de datos
def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root', 
        password='', 
        db='reservas_restaurantes',
        cursorclass=pymysql.cursors.DictCursor
    )
# -------------------------------
# 🔹 LOGIN CLIENTE
# -------------------------------
@app.route('/login-cliente', methods=['GET', 'POST'])
def loginCliente():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conexion = get_db_connection()
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
@app.route('/dashboard-cliente')
def dashboard_cliente():
    if 'cliente_id' in session:
        return render_template("reserva/nueva-reserva.html")
    else:
        return redirect(url_for('loginCliente'))


    
@app.route('/registro-cliente',methods=['GET'])
def registroCliente():
    return render_template("registro/registro-cliente.html")
   

if __name__ == '__main__':    
    app.run(debug=True,port=80)
