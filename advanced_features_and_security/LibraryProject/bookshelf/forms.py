from django import forms
from .models import Book

class ExampleForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, label="Name")
    email = forms.EmailField(required=True, label="Email")
    message = forms.CharField(widget=forms.Textarea, required=False, label="Message")