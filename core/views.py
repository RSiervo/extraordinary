from django.shortcuts import render, redirect
from .models import FeaturedPost
from .forms import NewsletterForm, ContactForm
from django.contrib import messages
from .models import Gallery

def gallery_view(request):
    gallery = Gallery.objects.all().order_by('-created_at')
    return render(request, 'core/gallery.html', {'gallery': gallery})


def home(request):
    return render(request, 'core/home.html')

def about(request):
    return render(request, 'core/about.html')

def videos(request):
    features = FeaturedPost.objects.all().order_by('-created_at')
    return render(request, 'core/videos.html', {'features': features})


def gallery(request):
    return render(request, 'core/gallery.html')

def photos(request):
    return render(request, 'core/photos.html')

def contact(request):
    return render(request, 'core/contact.html')

def join(request):
    return render(request, 'core/join.html')

def home(request):
    posts = FeaturedPost.objects.order_by('-created_at')[:6]
    nform = NewsletterForm()
    cform = ContactForm()
    return render(request, 'core/home.html', {'posts': posts, 'nform': nform, 'cform': cform})

def subscribe(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thanks! You are subscribed.')
        else:
            messages.error(request, 'Unable to subscribe (maybe already subscribed).')
    return redirect('home')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Message sent. We will reach out soon.')
        else:
            messages.error(request, 'Please correct the form.')
    return redirect('home')
