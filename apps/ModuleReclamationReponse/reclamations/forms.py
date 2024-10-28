from django import forms
from .models import Reclamation, Reponse

class ReclamationForm(forms.ModelForm):
    class Meta:
        model = Reclamation
        fields = ['titre', 'description', 'priorite']  # Supprimez 'utilisateur'

    def clean_titre(self):
        titre = self.cleaned_data.get('titre')
        if not titre:
            raise forms.ValidationError("Le titre est obligatoire.")
        if len(titre) < 5:
            raise forms.ValidationError("Le titre doit contenir au moins 5 caractères.")
        return titre

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if not description:
            raise forms.ValidationError("La description est obligatoire.")
        return description
class ReponseForm(forms.ModelForm):
    class Meta:
        model = Reponse
        fields = ['texte', 'utilisateur', 'reclamation']
