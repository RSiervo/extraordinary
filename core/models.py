from django.db import models
from django.utils import timezone
from core.storage_backends import SupabaseStorage

supabase_storage = SupabaseStorage()


class FeaturedPost(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(storage=supabase_storage, upload_to='featured_images/', blank=True, null=True)
    video_url = models.URLField(blank=True, help_text="YouTube link (optional)")
    uploaded_video = models.FileField(storage=supabase_storage, upload_to='featured_videos/', blank=True, null=True, help_text="Upload a local video file (optional)")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class NewsletterSignup(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} <{self.email}>"


class Gallery(models.Model):
    title = models.CharField(max_length=200)
    anime_name = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    file = models.ImageField(storage=supabase_storage, upload_to='gallery/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
