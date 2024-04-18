from flask import Flask, render_template, request, redirect, url_for, flash
#from flask_sqlalchemy import SQLAlchemy
#from flask_login import LoginM logout_user, loginmanager, login_user,n_required, current_user, UserMixin

# Crear la aplicación Flask
app = Flask(__name__)

# Definir rutas y vistas
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/roles')
def roles():
    
    return render_template('roles.html')

@app.route('/login')
def login():
    
    return render_template('login.html')

@app.route('/registrar')
def registrar():
    
    return render_template('register.html')

# Punto de entrada para ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True, port=5000)
