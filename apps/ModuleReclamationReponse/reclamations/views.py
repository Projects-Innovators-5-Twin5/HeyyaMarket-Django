from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, CreateView
from .models import Reclamation, Reponse
from .forms import ReclamationForm, ReponseForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from web_project import TemplateLayout
from web_project.template_helpers.theme import TemplateHelper

class AjouterReclamationView(CreateView):
    model = Reclamation
    form_class = ReclamationForm
    template_name = 'reclamations/ajouter_reclamation.html'
    success_url = reverse_lazy('ReclamationFront')

    def form_valid(self, form):
        # Afficher les données du formulaire dans la console avant de les sauvegarder
        print("Titre:", form.cleaned_data['titre'])
        print("Description:", form.cleaned_data['description'])
        print("Priorité:", form.cleaned_data['priorite'])

        # Enregistrer explicitement l'objet avant le return
        self.object = form.save()  # Appel explicite à save()

        # Afficher l'objet sauvegardé dans la console
        print("Objet sauvegardé:", self.object)

        return super().form_valid(form)

    def form_invalid(self, form):
        # Afficher les erreurs dans la console si le formulaire n'est pas valide
        print("Le formulaire est invalide. Erreurs :", form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        # Mise à jour du contexte avec le chemin du layout
        context.update(
            {
                "layout_path": TemplateHelper.set_layout("layout_user.html", context),
            }
        )
        return context




class ListeReclamationsView(ListView):
    model = Reclamation
    template_name = 'reclamations/liste_reclamations.html'
    context_object_name = 'reclamations'
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        # Update the context
        context.update(
            {
                "layout_path": TemplateHelper.set_layout("layout_vertical.html", context),
            }
        )

        return context


from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from .models import Reclamation
from .forms import ReponseForm

from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.contrib.auth import get_user_model
from .models import Reclamation
from .forms import ReponseForm
from django.contrib import messages  # Ajoutez ceci en haut de votre fichier
User = get_user_model()  # Récupérer le modèle utilisateur

class RepondreReclamationView(View):
    def get(self, request, reclamation_id):
        reclamation = get_object_or_404(Reclamation, id=reclamation_id)
        form = ReponseForm()
        return render(request, 'reclamations/repondre_reclamation.html', {'form': form, 'reclamation': reclamation})

    def post(self, request, reclamation_id):
        reclamation = get_object_or_404(Reclamation, id=reclamation_id)
        form = ReponseForm(request.POST)

        if form.is_valid():
            reponse = form.save(commit=False)
            reponse.reclamation = reclamation

            utilisateur_id = reclamation.utilisateur_id  # Obtenir l'ID de l'utilisateur
            reponse.utilisateur = User.objects.get(id=utilisateur_id)  # Récupérer l'instance utilisateur

            reponse.save()
            messages.success(request, 'Votre réponse a été ajoutée avec succès.')  # Ajouter le message de succès
            #return redirect('liste_reclamations')

        return redirect('liste_reclamations')

class ModifierReclamationView(View):
    def get_object(self, reclamation_id):
        # Récupérer la réclamation spécifique
        return get_object_or_404(Reclamation, id=reclamation_id)

    def post(self, request, reclamation_id):
        # Récupérer la réclamation
        reclamation = self.get_object(reclamation_id)

        # Mettre à jour les champs de la réclamation avec les données soumises
        reclamation.titre = request.POST.get('titre')
        reclamation.description = request.POST.get('description')

        reclamation.statut = request.POST.get('statut')
        reclamation.save()  # Sauvegarder les modifications

        return redirect('liste_reclamations')  # Rediriger vers la liste après modification

    def get(self, request, reclamation_id):
        # Si l'on veut gérer un GET pour afficher des détails ou rediriger
        return redirect('liste_reclamations')
class SupprimerReclamationView(View):
    def post(self, request, reclamation_id):
        # Récupérer la réclamation à supprimer
        reclamation = get_object_or_404(Reclamation, id=reclamation_id)

        # Supprimer la réclamation
        reclamation.delete()

        # Rediriger vers la liste des réclamations après suppression
        return redirect('liste_reclamations')
class RechercheReclamations(View):
    def get(self, request):
        query = request.GET.get('query', '')
        reclamations = Reclamation.objects.filter(titre__icontains=query)
        results = [{'id': reclamation.id, 'titre': reclamation.titre, 'date_creation': reclamation.date_creation,
                    'priorite': reclamation.priorite, 'statut': reclamation.statut} for reclamation in reclamations]
        return JsonResponse(results, safe=False)
class ListeReclamationsFrontView(ListView):
    model = Reclamation
    template_name = 'reclamations/LIsteReclamation.html'
    context_object_name = 'reclamations'
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        # Update the context
        context.update(
            {
                "layout_path": TemplateHelper.set_layout("layout_user.html", context),
            }
        )

        return context
