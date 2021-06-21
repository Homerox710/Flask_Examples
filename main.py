from flask import Flask, request, make_response, redirect, render_template

app = Flask(__name__)

todos = ['Comprar café', 'Enviar solicitud de compra', 'Entregar video']

@app.route('/')
def index():
    user_ip = request.remote_addr #Vamos a guardar la ip del usuario en una cookie y devolvemos una respuesta de flask
    response = make_response(redirect('/hello')) #Redirigimos la respuesta a /hello
    response.set_cookie('user_ip',user_ip)
    return response

@app.route('/hello')
def hello():
    user_ip = request.cookies.get('user_ip') #Obtenemos la cookie que seteamos en index
    context = {
        'user_ip' : user_ip,
        'todos':todos
    }
    return render_template('hello.html', **context) #Diccionario expandido para referenciarlas directamente

