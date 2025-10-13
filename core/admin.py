from django.contrib import admin
from .models import FeaturedPost, NewsletterSignup, ContactMessage, Gallery

@admin.register(FeaturedPost)
class FeaturedPostAdmin(admin.ModelAdmin):
    list_display = ('title','created_at')

@admin.register(NewsletterSignup)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email','created_at')

@admin.register(ContactMessage)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name','email','created_at')

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'anime_name', 'created_at')
    search_fields = ('title', 'anime_name')
    list_filter = ('anime_name', 'created_at')