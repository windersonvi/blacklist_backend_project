from flask import Flask
from api.usuarios.usuarios import usuarios

app = Flask(__name__)
app.register_blueprint(usuarios)