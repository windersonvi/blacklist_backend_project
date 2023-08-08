from flask import Blueprint, request, make_response 
from db.database import supabaseConnection
from api.domain_validator.domain_validator_api import is_valid_email_format, is_valid_domain
import bcrypt
from datetime import date, datetime
import re
import secrets

usuarios = Blueprint('usuarios', __name__)

@usuarios.route("/register", methods=["POST"])
def register():
    
    salt = bcrypt.gensalt()
    data = request.get_json()

    mail_usuario = data.get("mail_usuario")
    name_usuario = data.get("name_usuario")
    pswd_usuario = data.get("pswd_usuario")
    tlfn_usuario = data.get("tlfn_usuario")
    birth_usuario = data.get("birth_usuario")
    id_plan = data.get("id_plan")

    if not is_valid_email_format(mail_usuario):
        return make_response({"error": "El formato del correo no es válido"}, 400)
    
    if not is_valid_domain(mail_usuario):
        return make_response({"error": "El dominio del correo no es válido"}, 400)

    if not is_valid_name(name_usuario):
        return make_response({"error": "El nombre solo puede contener letras"}, 400)
    
    #Validar que el correo no sea existente 
    validmail= supabaseConnection.table("usuario").select("mail_usuario").eq("mail_usuario",mail_usuario).execute()
    if validmail.data:
        return make_response({"error": "El correo ya existe"}, 400)
    
    #Validar si es mayor de edad
    today = date.today()
    nac = datetime.strptime(birth_usuario, "%Y-%m-%d")
    nac = nac.date()
    age = today - nac
    age = age.total_seconds() / (365.25 * 24 * 60 * 60)
    age = round(age)
    if age < 18:
        return make_response({"error": "El usuario debe ser mayor de edad"}, 400)

    #Generar api key del plan free 
    if id_plan == 1:
        api_key = secrets.token_urlsafe(12)

    if not is_valid_phone_number(tlfn_usuario):
        return make_response({"error": "Formato de teléfono inválido"}, 400)

    #Encriptacion
    hashed = bcrypt.hashpw(pswd_usuario.encode("utf-8"), salt)
    hashed = hashed.decode("utf-8")

    response = supabaseConnection.table("usuario").insert([
        {
            "mail_usuario": mail_usuario,
            "name_usuario": name_usuario,
            "pswd_usuario": hashed,
            "tlfn_usuario": tlfn_usuario,
            "birth_usuario": birth_usuario,
            "api_key": api_key,
            "id_plan": id_plan
        }
    ]).execute()

    supabaseConnection.table("request").insert([
        {
            "mail_usuario": mail_usuario,
            "num_request": 0
        }
    ]).execute()

    result = response.json()
    
    return make_response(result,200)

def is_valid_name(name):
    pattern = r"^[A-Za-z\s]+$"
    return re.match(pattern, name)

def is_valid_phone_number(phone):
    pattern = r"^[+][0-9]+$"
    return re.match(pattern, phone)

@usuarios.route("/login", methods=["POST"])
def login():
    salt = bcrypt.gensalt(10)

    data = request.get_json()
    mail_usuario = data.get("mail_usuario")
    pswd_usuario = data.get("pswd_usuario")

    hashed = bcrypt.hashpw(pswd_usuario.encode("utf-8"), salt)
    hashed = hashed.decode("utf-8")

    search = supabaseConnection.table("usuario").select("mail_usuario","pswd_usuario").eq("mail_usuario", mail_usuario).execute()
    if search.data:
        if bcrypt.checkpw(pswd_usuario, search.data[0]["pswd_usuario"]):
        #if hashed == search.data[0]["pswd_usuario"]:
            return make_response({"success": "usuario encontrado"}, 200)
        else: 
            return make_response({"error": "La clave es incorrecta"}, 400)
    else:
        return make_response({"error": "El correo no existe"}, 400)
