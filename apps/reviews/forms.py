# apps/reviews/forms.py

from django import forms
from .models import Avis, Commentaire

class AvisForm(forms.ModelForm):
    class Meta:
        model = Avis
        fields = ['rating', 'text']

class CommentaireForm(forms.ModelForm):
    class Meta:
        model = Commentaire
        fields = ['text']
