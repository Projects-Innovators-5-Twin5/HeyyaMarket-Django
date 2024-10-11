# apps/reviews/urls.py

from django.urls import path
from . import views
from .views import avis_list, stats_avis  # N'oublie pas d'importer ta nouvelle vue

urlpatterns = [
    path('avis/', views.avis_list, name='avis_list'),  # Afficher tous les avis du produit
        path('avis/stats/', stats_avis, name='stats_avis'),  # Nouvelle URL pour les stats

]
