from flask import Blueprint

#Esto significa que todas las rutas con /auth serán redirijidas acá
auth = Blueprint('auth',__name__, url_prefix='/auth')   

from . import views