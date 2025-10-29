import os
from django.core.files.storage import Storage
from django.core.files.base import ContentFile
from supabase import create_client, Client
from supabase.lib.client_options import ClientOptions

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET", "media")

# Initialize Supabase client
supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY,
    options=ClientOptions(auto_refresh_token=False)
)

class SupabaseStorage(Storage):
    def _save(self, name, content):
        """Uploads a file to Supabase Storage."""
        content.seek(0)
        data = content.read()

        try:
            # ✅ Upload raw bytes (no BytesIO, no file_options)
            response = supabase.storage.from_(SUPABASE_BUCKET).upload(name, data)

            # Check for any Supabase error in response
            if isinstance(response, dict) and response.get("error"):
                raise Exception(response["error"])
            elif "error" in str(response).lower():
                raise Exception(str(response))

        except Exception as e:
            raise Exception(f"Failed to upload '{name}' to Supabase: {e}")

        return name

    def exists(self, name):
        """Checks if the file already exists in Supabase bucket."""
        try:
            files = supabase.storage.from_(SUPABASE_BUCKET).list()
            return any(file["name"] == name for file in files)
        except Exception:
            return False

    def url(self, name):
        """Returns the public URL of the file."""
        return f"{SUPABASE_URL}/storage/v1/object/public/{SUPABASE_BUCKET}/{name}"

    def open(self, name, mode="rb"):
        """Downloads a file from Supabase Storage."""
        try:
            response = supabase.storage.from_(SUPABASE_BUCKET).download(name)
            if hasattr(response, "read"):
                return ContentFile(response.read())
            return ContentFile(response)
        except Exception as e:
            raise FileNotFoundError(f"File '{name}' not found in Supabase: {e}")
