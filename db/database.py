from supabase import create_client, Client
import os

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def insert_mail(email):
    data = supabase.table("blacklist").insert({"mail_blacklist":email}).execute()

