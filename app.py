from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, or_ , and_
import string
import random
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
    fondo_clase = conexion.Column(conexion.String(150))
    codigo_clase = conexion.Column(conexion.String(10))
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
    calificacion = conexion.Column(conexion.Integer)
    dificultad = conexion.Column(conexion.String(20))
    comentario = conexion.Column(conexion.String(200))
    estado = conexion.Column(conexion.String(30))
    clase = conexion.relationship("Tema")
    
class Inscripcion(conexion.Model):
    ID_usuario_clase = conexion.Column(conexion.Integer, primary_key=True, autoincrement=True)
    ID_usuario = conexion.Column(conexion.Integer, conexion.ForeignKey('usuario.ID_usuario'))
    ID_clase = conexion.Column(conexion.Integer, conexion.ForeignKey('clase.ID_clase'))
    usuario = conexion.relationship("Usuario")
    clase = conexion.relationship("Clase")
    
class Registro(conexion.Model):
    ID_registro = conexion.Column(conexion.Integer, primary_key=True)
    conteo_revision_f = conexion.Column(conexion.Integer, nullable=True)
    conteo_compartido_f = conexion.Column(conexion.Integer, nullable=True)
    ID_usuario = conexion.Column(conexion.Integer, conexion.ForeignKey('usuario.ID_usuario'))
    ID_flashcard = conexion.Column(conexion.Integer, conexion.ForeignKey('flashcard.ID_flashcard'))
    usuario = conexion.relationship("Usuario")
    flashcard = conexion.relationship("Flashcard")
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
             return redirect(url_for('clases'))
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
# /clases sirve para DOCENTE y ESTUDIANTE
@app.route('/clases')
def clases():
    global clases_filtradas
    clases_filtradas = conexion.session.query(Clase).join(Inscripcion).filter(Inscripcion.ID_usuario == logged_user.ID_usuario).all()
    if logged_user.rol == 'estudiante':
        return render_template('/estudiante/e-panel-clases.html', clases=clases_filtradas)
    if logged_user.rol == 'docente':
        return render_template('/docente/d-panel-clases.html', clases=clases_filtradas)

@app.route('/clases/unirse', methods=['POST', 'GET'])
def unirse():
    if request.method == 'POST':
        codigo_ingresado = request.form['codigo']
        codigo_filtrado = Clase.query.filter_by(codigo_clase=codigo_ingresado).first()
        if codigo_filtrado:
            nueva_inscripcion = Inscripcion(ID_usuario=logged_user.ID_usuario, ID_clase=codigo_filtrado.ID_clase)
            conexion.session.add(nueva_inscripcion)
            conexion.session.commit()
        ##else agregar mensaje flash
            
            return redirect('/clases')
    return redirect('/clases')      
    
@app.route('/temas/<idClase>')
def temas(idClase):
    global clase_seleccionada
    clase_seleccionada = Clase.query.filter_by(ID_clase=idClase).first()
    temas_filtrados = Tema.query.filter_by(ID_clase=clase_seleccionada.ID_clase) ##Cambiar la BD en esta parte
    if temas_filtrados and logged_user.rol == 'estudiante':
        return render_template('/estudiante/e-panel-temas.html', temas=temas_filtrados, clases = clases_filtradas, clase_seleccionada=clase_seleccionada)
    if temas_filtrados and logged_user.rol == 'docente':
        return render_template('/docente/d-panel-temas.html', temas=temas_filtrados, clases = clases_filtradas, clase_seleccionada=clase_seleccionada) #Manejo de errores

@app.route('/flash/<idTema>')
def flash(idTema):
    mostrar = False
    global flash_filtradas
    global tema_seleccionado
    tema_seleccionado = Tema.query.filter_by(ID_tema=idTema).first()
    flash_filtradas = Flashcard.query.filter_by(ID_tema=tema_seleccionado.ID_tema) ##Hay que cambiar
    if flash_filtradas and logged_user.rol == 'estudiante':
        return render_template('/estudiante/e-panel-flashcards.html', flashcards=flash_filtradas, clases = clases_filtradas, mostrar = mostrar, clase_seleccionada=clase_seleccionada, tema_seleccionado=tema_seleccionado)
    if flash_filtradas and logged_user.rol == 'docente':
        return render_template('/docente/d-panel-flashcards.html', flashcards=flash_filtradas, clases = clases_filtradas, mostrar = mostrar, clase_seleccionada=clase_seleccionada, tema_seleccionado=tema_seleccionado)
    
@app.route('/flashcard/<idFlash>')
def flashcard(idFlash):
    mostrar =True
    global flashcard_seleccionada
    flashcard_seleccionada = Flashcard.query.filter_by(ID_flashcard=idFlash).first()
    if flashcard_seleccionada and logged_user.rol == 'estudiante':
        return render_template('estudiante/e-panel-flashcards.html', flashcard_seleccionada=flashcard_seleccionada, clases = clases_filtradas, mostrar = mostrar, flashcards=flash_filtradas, clase_seleccionada=clase_seleccionada, tema_seleccionado=tema_seleccionado)
    if flashcard_seleccionada and logged_user.rol == 'docente':
        return render_template('docente/d-panel-flashcards.html', flashcard_seleccionada=flashcard_seleccionada, clases = clases_filtradas, mostrar = mostrar, flashcards=flash_filtradas, clase_seleccionada=clase_seleccionada, tema_seleccionado=tema_seleccionado)
    return render_template('register.html') #Manejo de errores

@app.route('/cambiar_dificultad/<idFlash>/<dificultad>')
def seleccionar_dificultad(idFlash, dificultad):
    url = '/flashcard/{}'.format(idFlash)
    conexion.session.query(Flashcard).filter_by(ID_flashcard=flashcard_seleccionada.ID_flashcard).update({"dificultad": dificultad})
    conexion.session.commit()
    return redirect(url)
   
@app.route('/enviar_revision/<idFlash>')
def enviar_revision(idFlash):
    url = '/flashcard/{}'.format(idFlash)
    if (flashcard_seleccionada.estado != 'compartido'):
        if(flashcard_seleccionada.estado == 'privado'):
            conexion.session.query(Flashcard).filter_by(ID_flashcard=flashcard_seleccionada.ID_flashcard).update({"estado": 'revision'})
            conexion.session.commit()
        else:
            conexion.session.query(Flashcard).filter_by(ID_flashcard=flashcard_seleccionada.ID_flashcard).update({"estado": 'privado'})
            conexion.session.commit()
        
    return redirect(url)

@app.route('/flashcard/crear', methods=['POST'])
def crearFlash():
    url = '/flash/{}'.format(tema_seleccionado.ID_tema)
    if request.method == 'POST':
        nueva_pregunta = request.form['pregunta']
        nueva_respuesta = request.form['respuesta']
        
        nueva_flashcard = Flashcard(pregunta=nueva_pregunta, respuesta=nueva_respuesta, ID_tema=tema_seleccionado.ID_tema, estado='privado')
        conexion.session.add(nueva_flashcard)
        conexion.session.commit()
        nuevo_registro = Registro(conteo_revision_f=0, conteo_compartido_f=0, ID_usuario=logged_user.ID_usuario, ID_flashcard=nueva_flashcard.ID_flashcard)
        conexion.session.add(nuevo_registro)
        conexion.session.commit()
        return redirect(url)
    return redirect(url)
    
    ####ROL DOCENTE
    
@app.route('/clases/crear', methods=['POST'])
def crearClase():
   # url = '/flash/{}'.format(tema_seleccionado.ID_tema)
    if request.method == 'POST':
        nuevo_titulo = request.form['titulo']
        nuevo_fondo = request.form['fondo']
        nuevo_color = request.form['color']
        
        nueva_clase = Clase(nombre_clase=nuevo_titulo, color_clase=nuevo_color, fondo_clase=nuevo_fondo, ID_usuario=logged_user.ID_usuario, codigo_clase=generarCodigo())
        conexion.session.add(nueva_clase)
        conexion.session.commit()
        nuevo_usuario_clase = Inscripcion(ID_usuario=logged_user.ID_usuario, ID_clase=nueva_clase.ID_clase)
        conexion.session.add(nuevo_usuario_clase)
        conexion.session.commit()
            
        return redirect('/clases')
    return redirect('/clases')  

@app.route('/temas/crear', methods=['POST'])
def crearTema():
   # url = '/flash/{}'.format(tema_seleccionado.ID_tema)
    if request.method == 'POST':
        nuevo_titulo = request.form['titulo']
        
        nuevo_tema = Tema(nombre_tema=nuevo_titulo, ID_clase=clase_seleccionada.ID_clase)
        conexion.session.add(nuevo_tema)
        conexion.session.commit()
        
        return redirect(f'/temas/{clase_seleccionada.ID_clase}')
    return redirect(f'/temas/{clase_seleccionada.ID_clase}') 

@app.route('/lista_estudiantes')
def lista_estudiantes():
    
    estudiantes_filtrados = conexion.session.query(Usuario).join(Inscripcion).filter(Usuario.rol == 'estudiante').all()
   
    return render_template('/docente/d-lista-estudiantes.html', clases = clases_filtradas, clase_seleccionada=clase_seleccionada, estudiantes=estudiantes_filtrados)

@app.route('/panel_revision/<idEstudiante>')
def panel_revision(idEstudiante):
    global estudiante_encontrado
    global estudiante
    
    #url = '/flashcard/{}'.format(idFlash)
    estudiante = Usuario.query.filter_by(ID_usuario=idEstudiante).first()
    
    ##Pendiente hacer el query para buscard por idEstudiante el temas de las flashcards
    estudiante_encontrado = conexion.session.query(Flashcard).join(Registro).filter(Registro.ID_usuario == idEstudiante, or_(Flashcard.estado == 'revision', Flashcard.estado == 'compartido')).all() 
    
    
    #estudiante_encontrado = conexion.session.query(Flashcard, Usuario).join(Registro, Registro.ID_flashcard == Flashcard.ID_flashcard).join(Usuario, Registro.ID_usuario == Usuario.ID_usuario).filter(Registro.ID_usuario == idEstudiante, or_(Flashcard.estado == 'revision', Flashcard.estado == 'compartido')).all()
    return render_template('/docente/d-panel-revision.html', clases = clases_filtradas, clase_seleccionada=clase_seleccionada, estudiante_encontrado=estudiante_encontrado, estudiante=estudiante)

@app.route('/panel_revision_flash/<idFlash>')
def revision_flash(idFlash):
    mostrar =True
    global tema_estudiante
    global flashcard_revision_seleccionada
    #tema_estudiante = Tema.query.filter_by(ID_tema=estudiante_encontrado.ID_tema).first()
    tema_estudiante = conexion.session.query(Tema).join(Flashcard).filter(Flashcard.ID_flashcard == idFlash).first()
    flashcard_revision_seleccionada = Flashcard.query.filter_by(ID_flashcard=idFlash).first()
    return render_template('docente/d-panel-revision.html', clases = clases_filtradas, clase_seleccionada=clase_seleccionada, estudiante_encontrado=estudiante_encontrado, flashcard_revision_seleccionada=flashcard_revision_seleccionada, mostrar=mostrar, estudiante=estudiante, tema_estudiante=tema_estudiante)
    
@app.route('/seleccionar_estado/<idFlash>/<estado>/<panel>')
def seleccionar_estado(idFlash, estado, panel):
    if(panel=='flash_compartida'):
        url = '/seleccionar_resultado_flash/{}'.format(idFlash) 
        conexion.session.query(Flashcard).filter_by(ID_flashcard=flashcard_compartida_seleccionada.ID_flashcard).update({"estado": estado}) 
    else:
        url = '/panel_revision_flash/{}'.format(idFlash)
        conexion.session.query(Flashcard).filter_by(ID_flashcard=flashcard_revision_seleccionada.ID_flashcard).update({"estado": estado})
    
    conexion.session.commit()
    return redirect(url)



@app.route('/biblioteca_compartida')
def biblioteca_compartida(): 
    flashcards_compartidas = (
    conexion.session.query(Flashcard)
    .join(Tema, Tema.ID_tema == Flashcard.ID_tema)
    .join(Clase, Clase.ID_clase == Tema.ID_clase)
    .filter(
         and_(
            Flashcard.estado == 'compartido',
            Clase.ID_clase == clase_seleccionada.ID_clase
            )
        )
    .all()
    )
    #estudiante_encontrado = conexion.session.query(Flashcard, Usuario).join(Registro, Registro.ID_flashcard == Flashcard.ID_flashcard).join(Usuario, Registro.ID_usuario == Usuario.ID_usuario).filter(Registro.ID_usuario == idEstudiante, or_(Flashcard.estado == 'revision', Flashcard.estado == 'compartido')).all()
    return render_template('/docente/d-biblioteca-compartida.html', clases = clases_filtradas, clase_seleccionada=clase_seleccionada, flashcards_compartidas=flashcards_compartidas)

@app.route('/seleccionar_resultado_flash/<idFlash>')
def compartido_flash(idFlash):
    mostrar =True
    global flashcard_compartida_seleccionada
    usuario_compartido = (
    conexion.session.query(Usuario)
    .join(Registro, Registro.ID_usuario == Usuario.ID_usuario)
    .join(Flashcard, Flashcard.ID_flashcard == Registro.ID_flashcard)
    .filter(Flashcard.ID_flashcard == idFlash).first())
    
    tema_estudiante_compartido = conexion.session.query(Tema).join(Flashcard).filter(Flashcard.ID_flashcard == idFlash).first()
    flashcard_compartida_seleccionada = Flashcard.query.filter_by(ID_flashcard=idFlash).first()
    return render_template('/docente/d-biblioteca-compartida.html', clases = clases_filtradas, clase_seleccionada=clase_seleccionada, flashcard_compartida_seleccionada=flashcard_compartida_seleccionada, mostrar=mostrar, tema_estudiante_compartido=tema_estudiante_compartido, usuario_compartido=usuario_compartido)

def generarCodigo():
    caracteres = string.ascii_uppercase + string.digits  
    codigo_generado = ''.join(random.choice(caracteres) for _ in range(6))
    codigos_filtrados = Clase.query.filter_by(codigo_clase=codigo_generado).all()
    if codigos_filtrados:
        codigo_generado = generarCodigo()
    else:
        return codigo_generado
    
# Punto de entrada para ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True, port=5000)
