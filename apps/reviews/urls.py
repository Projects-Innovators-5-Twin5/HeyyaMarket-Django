# apps/reviews/urls.py

from django.urls import path
from . import views
from .views import avis_list, stats_avis  # N'oublie pas d'importer ta nouvelle vue
from .views import backoffice_reviews  # Assurez-vous d'importer votre vue

urlpatterns = [
    path('avis/<int:product_id>/', views.avis_list, name='avis_list'),  # Afficher tous les avis du produit
    path('avis/stats/<int:product_id>/', stats_avis, name='stats_avis'),  # Nouvelle URL pour les stats avec product_id
    path('backoffice/reviews/<int:product_id>/', backoffice_reviews, name='backoffice_reviews'),  # URL pour le backoffice

]
