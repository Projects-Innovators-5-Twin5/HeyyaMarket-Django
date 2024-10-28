# authentication/forms.py
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from .models import User

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=63,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez votre username','id': 'username'})
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


class BrandRequestForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['brand_name', 'brand_description', 'brand_email', 'brand_rne_number', 'brand_logo']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'tel', 'addresse', 'bio', 'role']  # Add the fields you want to update.

    # Custom error messages for each field
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name:
            raise ValidationError('Le prénom est obligatoire *', code='required')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name:
            raise ValidationError('Le nom est obligatoire *', code='required')
        return last_name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise ValidationError('L\'email est obligatoire *', code='required')
        return email
