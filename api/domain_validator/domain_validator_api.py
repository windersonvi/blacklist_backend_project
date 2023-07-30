from flask import Blueprint, request
import re

domain_validator = Blueprint('domain_validator', __name__)

@domain_validator.route('/validate', methods="POST")
def index():
    email = request.form['email']
    if email != '' and validate_email_format(email):
        return True
    else:
        return False

def validate_email_format(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return True
    else:
        return False

