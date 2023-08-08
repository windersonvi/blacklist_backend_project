from flask import Flask
from api.domain_validator.domain_validator_api import domain_validator
from api.usuarios.usuarios import usuarios

app = Flask(__name__)
app.register_blueprint(domain_validator)
app.register_blueprint(usuarios)

