# authentication/forms.py
from django import forms 
from django.contrib.auth import get_user_model

from django.contrib.auth.forms import UserCreationForm
from .models import User

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=63, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez votre email ou username','id': 'username'})
    )
    password = forms.CharField(
        max_length=63, 
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Entrez votre mot de passe','id': 'password'})
    )



class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email', 'password1','password2','role')

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'  
            field.widget.attrs['placeholder'] = f'Entrez votre {field.label.lower()}'
  

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['bio', 'addresse', 'email', 'tel', 'profile_photo', 'first_name', 'last_name']
