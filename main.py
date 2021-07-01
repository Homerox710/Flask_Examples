from flask import Flask, request, make_response, redirect, render_template, session, url_for, flash
from app.forms import LoginForm
import unittest
from flask_login import login_required, current_user
from app import create_app
from app.firestore_service import get_users, get_todos
app = create_app()

todos = ['Comprar café', 'Enviar solicitud de compra', 'Entregar video']



#Comando para testing
@app.cli.command()
def test():
    test = unittest.TestLoader().discover('test')
    unittest.TextTestRunner().run(test)


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

#Especificamos los métodos permitidos
@app.route('/hello', methods=['GET'])
@login_required
def hello():
    user_ip = session.get('user_ip') #Obtenemos la ip de session
    username = current_user.id
    context = {
        'user_ip' : user_ip,
        'todos': get_todos(user_id=username),
        'username': username
    }

    return render_template('hello.html', **context) #Diccionario expandido para referenciarlas directamente

