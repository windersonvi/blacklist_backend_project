#from flask import Flask

#app = Flask(__name__)

#@app.route("/")
#def hello_world():
#    return "<p>Hello, World!</p>"

from flask import Flask
from api.domain_validator.domain_validator_api import domain_validator

app = Flask(__name__)
app.register_blueprint(domain_validator)