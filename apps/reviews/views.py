from django.shortcuts import render, redirect, get_object_or_404
from .models import Avis, Commentaire
from .forms import AvisForm, CommentaireForm
from apps.authentication.models import User
from apps.gestion_produits.models import Product
from django.db.models import Avg, Count
from web_project.template_helpers.theme import TemplateHelper
from transformers import pipeline

# Charger le pipeline de sentiment multilingue
sentiment_pipeline = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

# Fonction pour analyser le sentiment d'un texte
def analyze_sentiment(text):
    result = sentiment_pipeline(text)
    score = result[0]["score"]
    label = result[0]["label"]

    if label == "1 star" or (label == "2 stars" and score > 0.6):
        sentiment = "très négatif"
    elif label == "2 stars":
        sentiment = "négatif"
    elif label == "3 stars":
        sentiment = "neutre"
    elif label == "4 stars":
        sentiment = "légèrement positif"
    elif label == "5 stars" or (label == "4 stars" and score > 0.6):
        sentiment = "très positif"
    else:
        sentiment = "neutre"

    return sentiment, score


def avis_list(request, product_id):
    # Récupérer les avis pour le produit
    avis = Avis.objects.filter(product_id=product_id)
    product = get_object_or_404(Product, id=product_id)

    # Calcul des étoiles restantes et analyse de sentiment pour chaque avis
    for a in avis:
        a.remaining_stars = 5 - a.rating  # Ajouter les étoiles restantes
        sentiment_result = analyze_sentiment(a.text)
        a.sentiment = sentiment_result[0]  # Sentiment en texte
        a.sentiment_score = sentiment_result[1]  # Score de confiance

    avis_form = AvisForm()
    commentaire_form = CommentaireForm()

    if request.method == 'POST':
        if 'avis_submit' in request.POST:
            avis_form = AvisForm(request.POST)
            if avis_form.is_valid():
                new_avis = avis_form.save(commit=False)
                new_avis.user = request.user
                new_avis.product_id = product_id
                new_avis.save()
                return redirect('avis_list', product_id=product_id)

        elif 'commentaire_submit' in request.POST:
            avis_id = request.POST.get('avis_id')
            avis_instance = get_object_or_404(Avis, id=avis_id)
            commentaire_form = CommentaireForm(request.POST)
            if commentaire_form.is_valid():
                new_commentaire = commentaire_form.save(commit=False)
                new_commentaire.user = request.user
                new_commentaire.avis = avis_instance
                new_commentaire.save()
                return redirect('avis_list', product_id=product_id)

        elif 'avis_edit' in request.POST:
            avis_id = request.POST.get('avis_id')
            avis_instance = get_object_or_404(Avis, id=avis_id)
            avis_form = AvisForm(request.POST, instance=avis_instance)
            if avis_form.is_valid():
                avis_form.save()
                return redirect('avis_list', product_id=product_id)

        elif 'commentaire_edit' in request.POST:
            commentaire_id = request.POST.get('commentaire_id')
            commentaire_instance = get_object_or_404(Commentaire, id=commentaire_id)
            commentaire_form = CommentaireForm(request.POST, instance=commentaire_instance)
            if commentaire_form.is_valid():
                commentaire_form.save()
                return redirect('avis_list', product_id=product_id)

        elif 'avis_delete' in request.POST:
            avis_id = request.POST.get('avis_id')
            avis_instance = get_object_or_404(Avis, id=avis_id)
            avis_instance.delete()
            return redirect('avis_list', product_id=product_id)

        elif 'commentaire_delete' in request.POST:
            commentaire_id = request.POST.get('commentaire_id')
            commentaire_instance = get_object_or_404(Commentaire, id=commentaire_id)
            commentaire_instance.delete()
            return redirect('avis_list', product_id=product_id)

    # Contexte pour le rendu
    context = {
        'avis': avis,
        'avis_form': avis_form,
        'commentaire_form': commentaire_form,
        'produit': product
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
