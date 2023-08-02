from flask import Blueprint, request
import db.database
import re
from supabase import create_client, Client
import os

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

domain_validator = Blueprint('domain_validator', __name__)

@domain_validator.route('/validate', methods=["POST"])
def index():
    email = request.form['email']
    if email != '' and validate_email_format(email):
        return {"message": "valido"}
    else:
        return {"message": "no valido"}

def validate_email_format(email):
    #pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    #pattern = r"^[a-zA-Z0-9_%+-]+(?:\.[a-zA-Z0-9_%+-]+)*@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    #pattern = r"^[a-zA-Z0-9_-]+(?:\.[a-zA-Z0-9_-]+)*@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    #pattern = r"^(?!.*[._-]{2})[a-zA-Z0-9_-]+(?:\.[a-zA-Z0-9_-]+)*@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    pattern = r"^(?!.*[._-]{2})(?!.*-\.|\.-|-_|__)[a-zA-Z0-9_-]+(?:\.[a-zA-Z0-9_-]+)*@[a-zA-Z0-9]+(?:[-.][a-zA-Z0-9]+)*\.(?!-)[a-zA-Z]{2,}$"
    if re.match(pattern, email):
        return True
    else:
        return False

@domain_validator.route('/insert-mail', methods=["POST"])
def insert_mail():
    email = request.form['email']
    data = insert_mail(email)
    return data

def insert_mail(email):
    data = supabase.table("blacklist").insert({"mail_blacklist":email}).execute()