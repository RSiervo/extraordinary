from django import forms
from .models import NewsletterSignup, ContactMessage
class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterSignup
        fields = ['email']
class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name','email','message']
