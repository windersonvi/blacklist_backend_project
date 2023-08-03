from flask import Blueprint, request, make_response, jsonify
from db.database import supabaseConnection
import re

domain_validator = Blueprint('domain_validator', __name__)

@domain_validator.route('/validate', methods=["POST"])
def index():
    email = request.form['email']
    if email != '' and is_valid_email_format(email):
        return make_response(jsonify({"error": True, "message":  "formato inválido"}), 400)
    else:
        return make_response(jsonify({"error": False, "message":  "formato válido"}), 200)

def is_valid_email_format(email):
    pattern = r"^(?!.*[._-]{2})(?!.*-\.|\.-|-_|__)[a-zA-Z0-9_-]+(?:\.[a-zA-Z0-9_-]+)*@[a-zA-Z0-9]+(?:[-.][a-zA-Z0-9]+)*\.(?!-)[a-zA-Z]{2,}$"
    if re.match(pattern, email):
        return True
    else:
        return False
    

@domain_validator.route('/validate-domain', methods=["POST"])  
def validate_domain():
    email = request.form['email']
    validDomain = is_valid_domain(email)
   
    if not validDomain:
        response = {"error": True, "message":  "dominio inválido"}
        return  make_response(jsonify(response), 400)
    
    return  make_response(jsonify({"error": False, "message":  "dominio válido"}), 200)

def is_valid_domain(email):
    emailDomain = email.partition('@')[2]
    domainValidation = findInvalidDomain(emailDomain)
    if len(domainValidation.data) > 0:
        return False
    
    return True

def insert_mail_blacklist(email):
    data = supabaseConnection.table("blacklist").insert({"mail_blacklist":email}).execute()


def findInvalidDomain(domain):
    return supabaseConnection.table("blacklist").select("mail_blacklist").eq("mail_blacklist", domain).execute()