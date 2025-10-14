import os
from supabase import create_client, Client
from django.core.files.storage import Storage
from django.conf import settings

class SupabaseStorage(Storage):
    def __init__(self):
        self.supabase: Client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_KEY
        )
        self.bucket_name = getattr(settings, 'SUPABASE_BUCKET', 'media')

    def _save(self, name, content):
        data = content.read()
        self.supabase.storage.from_(self.bucket_name).upload(name, data)
        return name

    def url(self, name):
        public_url = self.supabase.storage.from_(self.bucket_name).get_public_url(name)
        return public_url

    def exists(self, name):
        # Optional: check if the file already exists
        res = self.supabase.storage.from_(self.bucket_name).list()
        return any(f['name'] == name for f in res)
