from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
#from flask_login import LoginM logout_user, loginmanager, login_user,n_required, current_user, UserMixin

# Crear la aplicación Flask
app = Flask(__name__)
app.secret_key = 'mundolibre'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:mundolibre@localhost/chkdsk7$flashcards'
app.config['SECRET_KEY'] = 'mundolibre'
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

class Flashcard(conexion.Model):
    ID_flashcard = conexion.Column(conexion.Integer, primary_key=True, autoincrement=True)
    pregunta = conexion.Column(conexion.String(200))
    respuesta = conexion.Column(conexion.String(200))
    ID_tema = conexion.Column(conexion.Integer, conexion.ForeignKey('tema.ID_tema'))
    clase = conexion.relationship("Tema")
    
class UsuarioClase(conexion.Model):
    ID_usuario_clase = conexion.Column(conexion.Integer, primary_key=True, autoincrement=True)
    ID_usuario = conexion.Column(conexion.Integer, conexion.ForeignKey('usuario.ID_usuario'))
    ID_clase = conexion.Column(conexion.Integer, conexion.ForeignKey('clase.ID_clase'))
    codigo = conexion.Column(conexion.String(10))
    usuario = conexion.relationship("Usuario")
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
    global clases_filtradas
    clases_filtradas = Clase.query.filter_by(ID_usuario=logged_user.ID_usuario) #Join
    if clases_filtradas:
        return render_template('/panel-clases.html', clases=clases_filtradas)
        
@app.route('/temas/<idClase>')
def temas(idClase):
    global clase_seleccionada
    clase_seleccionada = Clase.query.filter_by(ID_clase=idClase).first()
    temas_filtrados = Tema.query.filter_by(ID_clase=clase_seleccionada.ID_clase)
    if temas_filtrados:
        return render_template('panel-temas.html', temas=temas_filtrados, clases = clases_filtradas, clase_seleccionada=clase_seleccionada)
    else:
        return render_template('register.html') #Manejo de errores

@app.route('/flash/<idTema>')
def flash(idTema):
    mostrar = False
    global flash_filtradas
    global tema_seleccionado
    tema_seleccionado = Tema.query.filter_by(ID_tema=idTema).first()
    flash_filtradas = Flashcard.query.filter_by(ID_tema=tema_seleccionado.ID_tema) ##Hay que cambiar
    if flash_filtradas:
        return render_template('panel-flashcards.html', flashcards=flash_filtradas, clases = clases_filtradas, mostrar = mostrar, clase_seleccionada=clase_seleccionada, tema_seleccionado=tema_seleccionado)
    else:
        return render_template('register.html') #Manejo de errores
    
@app.route('/flashcard/<idFlash>')
def flashcard(idFlash):
    mostrar =True
    flashcard_seleccionada = Flashcard.query.filter_by(ID_flashcard=idFlash).first()
    if flashcard_seleccionada:
        return render_template('panel-flashcards.html', flashcard_seleccionada=flashcard_seleccionada, clases = clases_filtradas, mostrar = mostrar, flashcards=flash_filtradas, clase_seleccionada=clase_seleccionada, tema_seleccionado=tema_seleccionado)
    else:
        return render_template('register.html') #Manejo de errores

@app.route('/flashcard/crear', methods=['POST'])
def crearFlash():
    url = '/flash/{}'.format(tema_seleccionado.ID_tema)
    if request.method == 'POST':
        nueva_pregunta = request.form['pregunta']
        nueva_respuesta = request.form['respuesta']
        
        nueva_flashcard = Flashcard(pregunta=nueva_pregunta, respuesta=nueva_respuesta, ID_tema=tema_seleccionado.ID_tema)
        conexion.session.add(nueva_flashcard)
        conexion.session.commit()
        
        return redirect(url)
    return redirect(url)
    
    ####ROL DOCENTE
    
    
    
# Punto de entrada para ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True, port=5000)
