from flask import Blueprint, request, make_response, jsonify, abort
from db.database import supabaseConnection
import re
from functools import wraps

domain_validator = Blueprint('domain_validator', __name__)

@domain_validator.route('/validate-email', methods=["POST"])
def validate_email():
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
    domainValidation = find_invalid_domain(emailDomain)
    if len(domainValidation.data) > 0:
        return False
    
    return True

def insert_mail_blacklist(email):
    data = supabaseConnection.table("blacklist").insert({"mail_blacklist":email}).execute()

def find_invalid_domain(domain):
    return supabaseConnection.table("blacklist").select("mail_blacklist").eq("mail_blacklist", domain).execute()

def require_api_key(view_function):
    @wraps(view_function)
    def verify_api_key(*args, **kwargs):
        api_key = request.headers.get('API-KEY')
        if not api_key:
            abort(401, 'API key is missing')
        if not is_valid_APIKEY(api_key):
            abort(401, 'Invalid API key')
        return view_function(*args, **kwargs)
    return verify_api_key

def is_valid_APIKEY(api_key):
    data = supabaseConnection.table("usuario").select("api_key").eq("api_key", api_key).execute()
    if len(data.data) > 0:
        return True
    
    return False

@domain_validator.route('/verify_email', methods=['POST'])
@require_api_key
def verifiy_email():
    api_key = request.headers.get('API-KEY')
    email = request.form['email']

    if email == '' and not is_valid_email_format(email):
        return make_response(jsonify({"error": True, "message":  "Límite de request excedido"}), 400)
    
    user_data = get_user_info(api_key)
    id_user = user_data['mail_usuario']
    user_plan_info = get_user_plan(user_data['id_plan'])
    requests_user = get_user_requests(id_user)

    if requests_user > user_plan_info['limit_plan']:
        return make_response(jsonify({"error": True, "message":  "Límite de request excedido"}), 400)
    
    validDomain = is_valid_domain(email)
   
    if not validDomain:
        return  make_response(jsonify({"error": True, "message":  "dominio inválido"}), 400)
    else:
        sum_request(id_user, requests_user)
        return  make_response(jsonify({"error": False, "message":  "dominio válido"}), 200)
    

def get_user_info(api_key):
    data = supabaseConnection.table("usuario").select("mail_usuario","id_plan").eq("api_key", api_key).execute()
    if len(data.data) > 0:
        return data.data[0]
    return False

def get_user_plan(id_plan):
    user_plan_info = supabaseConnection.table("plan").select("*").eq("id_plan", id_plan).execute()
    return user_plan_info.data[0]

def get_user_requests(id_user):
    user_requests = supabaseConnection.table("request").select("num_request").eq("mail_usuario", id_user).execute()
    return user_requests.data[0]['num_request']

def sum_request(id_user, user_requests):
    supabaseConnection.table("request").update({"num_request": user_requests + 1}).eq("mail_usuario", id_user).execute()
    