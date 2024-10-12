from django.shortcuts import render, redirect, get_object_or_404
from .models import Avis, Commentaire
from .forms import AvisForm, CommentaireForm
from apps.authentication.models import User
from django.db.models import Avg, Count
from web_project.template_helpers.theme import TemplateHelper
from web_project import TemplateLayout

def avis_list(request):
    # Récupérer les avis pour le produit avec ID statique 1
    avis = Avis.objects.filter(product_id=1)

    # Calculer les étoiles restantes pour chaque avis
    for a in avis:
        a.remaining_stars = 5 - a.rating  # Ajout d'une nouvelle propriété pour les étoiles restantes

    avis_form = AvisForm()
    commentaire_form = CommentaireForm()

    if request.method == 'POST':
        if 'avis_submit' in request.POST:
            # Soumission du formulaire d'avis
            avis_form = AvisForm(request.POST)
            if avis_form.is_valid():
                new_avis = avis_form.save(commit=False)
                new_avis.user = User.objects.get(id=1)  # Utilisateur statique avec id=1
                new_avis.product_id = 1  # Lier l'avis à un produit statique
                new_avis.save()
                return redirect('avis_list')

        elif 'commentaire_submit' in request.POST:
            # Soumission du formulaire de commentaire
            avis_id = request.POST.get('avis_id')
            avis_instance = get_object_or_404(Avis, id=avis_id)
            commentaire_form = CommentaireForm(request.POST)
            if commentaire_form.is_valid():
                new_commentaire = commentaire_form.save(commit=False)
                new_commentaire.user = User.objects.get(id=1)  # Utilisateur statique avec id=1
                new_commentaire.avis = avis_instance
                new_commentaire.save()
                return redirect('avis_list')

        elif 'avis_edit' in request.POST:
            # Soumission du formulaire de modification de l'avis
            avis_id = request.POST.get('avis_id')
            avis_instance = get_object_or_404(Avis, id=avis_id)
            avis_form = AvisForm(request.POST, instance=avis_instance)
            if avis_form.is_valid():
                avis_form.save()
                return redirect('avis_list')

    # Contexte pour le rendu
    context = {
        'avis': avis,
        'avis_form': avis_form,
        'commentaire_form': commentaire_form,
    }

    # Ajouter le chemin de mise en page
    context.update({
        "layout_path": TemplateHelper.set_layout("layout_user.html", context),
    })

    return render(request, 'avis_list.html', context)


def stats_avis(request):
    total_avis = Avis.objects.count()  # Nombre total d'avis
    average_rating = Avis.objects.aggregate(Avg('rating'))['rating__avg']  # Note moyenne

    # Comptage des notes (1 à 5)
    ratings_count = Avis.objects.values('rating').annotate(count=Count('id')).order_by('rating')
    ratings_data = [0] * 5  # Initialise une liste de 5 zéros pour les notes 1-5

    for rating in ratings_count:
        if 1 <= rating['rating'] <= 5:  # Vérifie que la note est entre 1 et 5
            ratings_data[rating['rating'] - 1] = rating['count']  # Remplit les données

    context = {
        'total_avis': total_avis,
        'average_rating': average_rating,
        'ratings_count': ratings_data,
    }

    return render(request, 'stats_avis.html', context)
