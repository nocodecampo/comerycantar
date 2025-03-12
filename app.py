from flask import Flask,render_template,request,redirect,url_for,session
import pymysql
import db


app = Flask(__name__)
app.secret_key="123456"


    
@app.route('/registro-cliente',methods=['GET'])
def registroCliente():
    return render_template("registro/registro-cliente.html")

@app.route('/registro-restaurante',methods=['GET'])
def registroRestaurante():
    return render_template("registro/registro-restaurante.html")

   
if __name__ == '__main__':    
    app.run(debug=True,port=80)
    

