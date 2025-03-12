from flask import Flask,render_template,request,redirect,url_for,session, flash
from werkzeug.security import check_password_hash
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
@app.route('/dashboard-cliente')
def dashboard_cliente():
    if 'cliente_id' in session:
        return render_template("reservas/nueva-reserva.html")
    else:
        return redirect(url_for('loginCliente'))
    
@app.route('/registro-cliente',methods=['GET'])#registro cliente
def registroCliente():
    return render_template("registro/registro-cliente.html")    

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

    


@app.route('/logout')
def logout():
    # Eliminar los datos de la sesión
    session.clear()  # Esto elimina todas las variables de sesión

    # Redirigir al login o a la página de inicio
    return redirect(url_for('loginCliente'))  # redirigir a  página de eleccion , de momento loginCliente , despues?->'home'
  

if __name__ == '__main__':    
    app.run(debug=True,port=80)
