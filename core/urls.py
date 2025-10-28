from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('about/', views.about, name='about'),
    path('videos/', views.videos, name='videos'),
    path('gallery/', views.gallery_view, name='gallery'),
    path('photos/', views.photos, name='photos'),
    path('contact/', views.contact, name='contact'),
    path('join/', views.join, name='join'),
]
