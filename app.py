from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
#from flask_login import LoginM logout_user, loginmanager, login_user,n_required, current_user, UserMixin

# Crear la aplicación Flask
app = Flask(__name__)
app.secret_key = 'mundolibre'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:mundolibre@localhost/chkdsk7$flashcards'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
conexion = SQLAlchemy(app)
estado_variable = ''
class Usuario(conexion.Model):
    ID_usuario = conexion.Column(conexion.Integer, primary_key=True, autoincrement=True)
    rol = conexion.Column(conexion.String(20))
    nombre_usuario = conexion.Column(conexion.String(30))
    contrasenia = conexion.Column(conexion.String(30))
    correo = conexion.Column(conexion.String(50))
    
class Clase(conexion.Model):
    ID_clase = conexion.Column(conexion.Integer, primary_key=True, autoincrement=True)
    nombre_clase = conexion.Column(conexion.String(40))
    color_clase = conexion.Column(conexion.String(30))
    ID_usuario = conexion.Column(conexion.Integer, conexion.ForeignKey('usuario.ID_usuario'))
    usuario = conexion.relationship("Usuario")

class Tema(conexion.Model):
    ID_tema = conexion.Column(conexion.Integer, primary_key=True, autoincrement=True)
    nombre_tema = conexion.Column(conexion.String(80))
    ID_clase = conexion.Column(conexion.Integer, conexion.ForeignKey('clase.ID_clase'))
    clase = conexion.relationship("Clase")
    
# Definir rutas y vistas
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/roles')
def roles():
    
    return render_template('roles.html')

@app.route('/vista_login')
def vista_login():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    global logged_user
    if request.method == 'POST':
        nombre_usuario = request.form['user']
        contrasenia = request.form['password']
        logged_user = Usuario.query.filter_by(nombre_usuario=nombre_usuario, contrasenia=contrasenia).first()
        
        if logged_user != None:
            if logged_user.rol == 'estudiante':
             return redirect(url_for('clases'))
            if logged_user.rol == 'docente':
             return redirect(url_for('login'))
        else:
            flash("No está registrado")
            return redirect(url_for('vista_login'))
    return render_template('roles.html')
   
@app.route('/vista_registrar')
def vista_registrar():
    return render_template('register.html')        
    
@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        nombre_usuario = request.form['user']
        contrasenia = request.form['password']
        correo = request.form['email']
        nuevo_usuario = Usuario(rol=estado_variable, nombre_usuario=nombre_usuario, contrasenia=contrasenia, correo=correo)
        conexion.session.add(nuevo_usuario)
        conexion.session.commit()
        return redirect('/')
    return redirect('/')

@app.route('/cambiar_estado_Estudiante', methods=['POST', 'GET'])
def cambiar_estado_Estudiante():
    global estado_variable
    estado_variable = 'estudiante'

    return render_template('register.html')

@app.route('/cambiar_estado_Docente', methods=['POST', 'GET'])
def cambiar_estado_Docente():
    global estado_variable
    estado_variable = 'docente'

    return render_template('register.html')

@app.route('/clases')
def clases():
    clases_filtradas = Clase.query.filter_by(ID_usuario=logged_user.ID_usuario) #Join
    if clases_filtradas:
        return render_template('/panel-clases.html', clases=clases_filtradas)
    
    
@app.route('/temas', methods=['GET', 'POST'])
def temas():
    clase_seleccionada = Clase.query.filter_by(ID_clase=request.form['valor'])
    temas_filtrados = Tema.query.filter_by(ID_clase=clase_seleccionada.ID_clase)
   
    if temas_filtrados:
        return render_template('panel-temas.html', temas=temas_filtrados)
        
    else:
        print("No se encontró ningúna clase")

    return redirect(url_for('clases'))


    
# Punto de entrada para ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True, port=5000)
