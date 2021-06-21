from flask import Flask, request, make_response, redirect, render_template, session
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = 'SUPER SECRETO'

todos = ['Comprar café', 'Enviar solicitud de compra', 'Entregar video']

# Manejar error 404 (not found)
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html',error=error) #Retornamos el html y una variable con la info del error

# Manejar error 500 (server)
@app.errorhandler(500)
def internal_server_error(error):
  return render_template('500.html')

@app.route('/')
def index():
    user_ip = request.remote_addr #Vamos a guardar la ip del usuario en una cookie y devolvemos una respuesta de flask
    response = make_response(redirect('/hello')) #Redirigimos la respuesta a /hello
    session['user_ip'] = user_ip #Solicitamos la ip por session para encriptar el dato
    return response

@app.route('/hello')
def hello():
    user_ip = session.get('user_ip') #Obtenemos la ip de session
    context = {
        'user_ip' : user_ip,
        'todos':todos
    }
    return render_template('hello.html', **context) #Diccionario expandido para referenciarlas directamente

