import os
from django.core.files.storage import Storage
from django.core.files.base import ContentFile
from supabase import create_client, Client
from supabase.lib.client_options import ClientOptions

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET", "media")

# Create the Supabase client
supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY,
    options=ClientOptions(auto_refresh_token=False)
)

class SupabaseStorage(Storage):
    def _save(self, name, content):
        """Uploads a file to Supabase Storage."""
        data = content.read()

        try:
            response = supabase.storage.from_(SUPABASE_BUCKET).upload(
                path=name,
                file=data,
                file_options={"upsert": True}  # Allows overwrite
            )

            if "error" in str(response).lower():
                raise Exception(f"Supabase upload error: {response}")

        except Exception as e:
            raise Exception(f"Failed to upload '{name}' to Supabase: {e}")

        return name

    def exists(self, name):
        """Checks if the file exists in Supabase bucket."""
        try:
            files = supabase.storage.from_(SUPABASE_BUCKET).list()
            return any(file["name"] == name for file in files)
        except Exception:
            return False

    def url(self, name):
        """Generates a public URL for the file."""
        return f"{SUPABASE_URL}/storage/v1/object/public/{SUPABASE_BUCKET}/{name}"

    def open(self, name, mode="rb"):
        """Fetches file content from Supabase."""
        try:
            response = supabase.storage.from_(SUPABASE_BUCKET).download(name)
            if hasattr(response, "read"):
                return ContentFile(response.read())
            return ContentFile(response)
        except Exception as e:
            raise FileNotFoundError(f"File '{name}' not found in Supabase: {e}")
