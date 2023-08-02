from flask import Flask, request, make_response
import supabase
import bcrypt
from datetime import date, datetime
#import re

app = Flask(__name__)

supabase_url = "https://wdofcdwwxujiqziftcbo.supabase.co"
supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Indkb2ZjZHd3eHVqaXF6aWZ0Y2JvIiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTA4MTMwMjUsImV4cCI6MjAwNjM4OTAyNX0.6B2406M5yxOT7wU60RnJUez-c9RGQXfx4xRjX3ASWAw"
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

    if not name_usuario.isalpha():
        return make_response({"error": "El nombre solo puede contener letras"}, 400)
    
    today = date.today()
    nac = datetime.strptime(birth_usuario, "%Y-%m-%d")
    nac = nac.date()
    age = today - nac
    age = age.total_seconds() / (365.25 * 24 * 60 * 60)
    age = round(age)
    if age < 18: # Puedes cambiar este valor según el criterio que quieras aplicar
        return make_response({"error": "El usuario debe ser mayor de edad"}, 400)
    
    #opcion 1:
    #if not re.match(r'^\\+?\\d+$', tlfn_usuario):
    # Mostrar un mensaje de error o pedir otro número
        #return make_response({"error": "El número de teléfono solo puede contener el signo + y dígitos"}, 400)

    #opcion 2
    #if not tlfn_usuario.isdigit():
    #    return make_response({"error": "El telefono solo puede contener numeros"}, 400)
    

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

    result = response.json()
    
    return make_response(result,200)