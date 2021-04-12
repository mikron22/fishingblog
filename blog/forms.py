from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from blog.models import Comment

class RegisterForm(UserCreationForm):
    image = forms.ImageField(label="Zdjęcie profilowe (opcjonalne)", required=False)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'image')

class CommentForm(forms.ModelForm):
    text = forms.CharField(label="Treść komentarza", required=True, widget=forms.Textarea, max_length=200)
    
    class Meta:
        model = Comment
        fields = ("text",)
