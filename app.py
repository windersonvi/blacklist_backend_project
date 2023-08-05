from flask import Flask, request, make_response 
import supabase
import bcrypt
from datetime import date, datetime
import re
import secrets

app = Flask(__name__)

supabase_url = "https://bbymnsnuaeecjusgxpkj.supabase.co"
supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJieW1uc251YWVlY2p1c2d4cGtqIiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTA4NDY5ODUsImV4cCI6MjAwNjQyMjk4NX0.uiZk349HrLwGYlE8-139YQ1MtQ9ZKjhKE5XGwG4fOV8"
client = supabase.create_client(supabase_url,supabase_key)

@app.route("/register", methods=["POST"])
def register():
    
    salt = bcrypt.gensalt()
    data = request.get_json()

    mail_usuario = data.get("mail_usuario")
    name_usuario = data.get("name_usuario")
    pswd_usuario = data.get("pswd_usuario")
    tlfn_usuario = data.get("tlfn_usuario")
    birth_usuario = data.get("birth_usuario")
    api_key = data.get("api_key")
    id_plan = data.get("id_plan")

    # Validar que sea solamente letras el nombre
    if not name_usuario.isalpha():
        return make_response({"error": "El nombre solo puede contener letras"}, 400)
    
    #Validar si es mayor de edad
    today = date.today()
    nac = datetime.strptime(birth_usuario, "%Y-%m-%d")
    nac = nac.date()
    age = today - nac
    age = age.total_seconds() / (365.25 * 24 * 60 * 60)
    age = round(age)
    if age < 18:
        return make_response({"error": "El usuario debe ser mayor de edad"}, 400)
    
    # Validar que el correo tenga un formato válido.
    format = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$')
    if not format.match(mail_usuario):
        return make_response({"error": "El formato del correo no es valido"}, 400)

    #Validar que el correo no sea existente 
    validmail= client.table("usuario").select("mail_usuario").eq("mail_usuario",mail_usuario).execute()
    if validmail.data:
        return make_response({"error": "El correo ya existe"}, 400)

    #Generar api key del plan free 
    if id_plan == 1:
        api_key = secrets.token_urlsafe(12)

    
    #opcion 1:
    #if not re.match(r'^\\+?\\d+$', tlfn_usuario):
    # Mostrar un mensaje de error o pedir otro número
        #return make_response({"error": "El número de teléfono solo puede contener el signo + y dígitos"}, 400)

    #opcion 2
    #if not tlfn_usuario.isdigit():
    #    return make_response({"error": "El telefono solo puede contener numeros"}, 400)

    #Encriptacion
    hashed = bcrypt.hashpw(pswd_usuario.encode("utf-8"), salt)
    hashed = hashed.decode("utf-8")

    response = client.table("usuario").insert([
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

    client.table("request").insert([
        {
            "mail_usuario": mail_usuario,
            "num_request": 0
        }
    ]).execute()

    result = response.json()
    
    return make_response(result,200)

