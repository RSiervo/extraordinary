import os
from django.core.files.storage import Storage
from django.core.files.base import ContentFile
from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET", "media")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class SupabaseStorage(Storage):
    def _save(self, name, content):
        # Upload the file to Supabase bucket
        data = content.read()
        supabase.storage.from_(SUPABASE_BUCKET).upload(name, data)
        return name

    def exists(self, name):
        try:
            supabase.storage.from_(SUPABASE_BUCKET).get_public_url(name)
            return False
        except Exception:
            return True

    def url(self, name):
        return f"{SUPABASE_URL}/storage/v1/object/public/{SUPABASE_BUCKET}/{name}"
