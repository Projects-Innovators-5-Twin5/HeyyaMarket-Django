from django import forms
from .models import Reclamation, Reponse

class ReclamationForm(forms.ModelForm):
    class Meta:
        model = Reclamation
        fields = ['titre', 'description', 'priorite']


class ReponseForm(forms.ModelForm):
    class Meta:
        model = Reponse
        fields = ['texte', 'utilisateur', 'reclamation']
