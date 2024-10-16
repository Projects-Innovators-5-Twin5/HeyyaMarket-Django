from django.urls import path
from .views import AjouterReclamationView,ListeReclamationsFrontView,SupprimerReclamationView,RechercheReclamations, ListeReclamationsView,ModifierReclamationView, RepondreReclamationView

urlpatterns = [
    path('ajouter/', AjouterReclamationView.as_view(), name='ajouter_reclamation'),
    path('', ListeReclamationsView.as_view(), name='liste_reclamations'),
    path('reclamations/', ListeReclamationsFrontView.as_view(), name='ReclamationFront'),
    path('repondre/<int:reclamation_id>/', RepondreReclamationView.as_view(), name='repondre_reclamation'),
    path('modifier_reclamation/<int:reclamation_id>/',ModifierReclamationView.as_view(), name='modifier_reclamation'),
    path('supprimer_reclamation/<int:reclamation_id>/', SupprimerReclamationView.as_view(), name='supprimer_reclamation'),
      path('recherchereclamations/', RechercheReclamations.as_view(), name='recherche_reclamations'),
]
