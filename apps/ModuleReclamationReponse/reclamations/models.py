from django.db import models
from apps.authentication.models import User
from django.conf import settings
from django.utils.timezone import now
class Reclamation(models.Model):
    titre = models.CharField(max_length=255)
    description = models.TextField()
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)  # Utiliser AUTH_USER_MODEL ici
    date_creation = models.DateTimeField(default=now)
    statut = models.CharField(default='en_attente', max_length=50, choices=[
        ('en_attente', 'En attente'),
        ('resolue', 'Résolue'),
        ('refusé', 'Refusée'),
    ])
    priorite = models.CharField(default='basse', max_length=50, choices=[
        ('basse', 'Basse'),
        ('moyenne', 'Moyenne'),
        ('elevee', 'Élevée'),
    ])

    def __str__(self):
        return self.titre

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class Reponse(models.Model):
    texte = models.TextField()
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)  # Utiliser AUTH_USER_MODEL ici
    reclamation = models.ForeignKey(Reclamation, on_delete=models.CASCADE)  # Relation avec Reclamation
    date_creation = models.DateTimeField(auto_now_add=True)
    est_approuvee = models.BooleanField(default=False)

    def __str__(self):
        return f"Réponse à {self.reclamation.titre}"
