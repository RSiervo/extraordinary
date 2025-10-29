import os
from io import BytesIO
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
        """Uploads a file to Supabase Storage safely."""
        try:
            # Ensure pointer is at start
            content.seek(0)
            data = BytesIO(content.read())

            # Upload file
            response = supabase.storage.from_(SUPABASE_BUCKET).upload(
                path=name,
                file=data,
                file_options={"content-type": "application/octet-stream", "upsert": True}
            )

            # Explicit error handling
            if hasattr(response, "error") and response.error:
                raise Exception(f"Supabase upload error: {response.error}")

        except Exception as e:
            raise Exception(f"Failed to upload '{name}' to Supabase: {e}")

        return name

    def exists(self, name):
        """Checks if the file exists in the bucket."""
        try:
            files = supabase.storage.from_(SUPABASE_BUCKET).list()
            return any(file.get("name") == name for file in files)
        except Exception:
            return False

    def url(self, name):
        """Returns the public URL of the file."""
        return f"{SUPABASE_URL}/storage/v1/object/public/{SUPABASE_BUCKET}/{name}"

    def open(self, name, mode="rb"):
        """Downloads file content."""
        try:
            response = supabase.storage.from_(SUPABASE_BUCKET).download(name)
            if hasattr(response, "read"):
                return ContentFile(response.read())
            return ContentFile(response)
        except Exception as e:
            raise FileNotFoundError(f"File '{name}' not found in Supabase: {e}")
