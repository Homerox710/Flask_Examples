from flask import Flask, request, make_response, redirect, render_template, session, url_for, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
import unittest

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = 'SUPER SECRETO'

todos = ['Comprar café', 'Enviar solicitud de compra', 'Entregar video']

class LoginForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Enviar')

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
@app.route('/hello', methods=['GET','POST'])
def hello():
    user_ip = session.get('user_ip') #Obtenemos la ip de session
    login_form = LoginForm()
    username = session.get('username')

    context = {
        'user_ip' : user_ip,
        'todos':todos,
        'login_form':login_form,
        'username': username
    }

    if login_form.validate_on_submit():
        username = login_form.username.data
        session['username'] = username
        flash('Nombre de usuario registrado con éxito!')
        return  redirect(url_for('index'))
    return render_template('hello.html', **context) #Diccionario expandido para referenciarlas directamente

