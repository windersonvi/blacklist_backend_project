from flask import Flask
from api.domain_validator.domain_validator_api import domain_validator

app = Flask(__name__)
app.register_blueprint(domain_validator)