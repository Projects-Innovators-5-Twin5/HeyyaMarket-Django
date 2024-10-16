from django.db import models
from apps.authentication.models import User
from django.conf import settings

class Avis(models.Model):
    product_id = models.IntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    likes = models.IntegerField(default=0)  # Champ pour stocker le nombre de J'aime
    text = models.TextField(null=True, blank=True)  # Rendre le champ nullable
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Avis de {self.user.username} - Note: {self.rating}"

class Commentaire(models.Model):
    avis = models.ForeignKey(Avis, on_delete=models.CASCADE, related_name='commentaires')  # L'avis auquel le commentaire appartient
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Utilise AUTH_USER_MODEL ici
    text = models.TextField()  # Le texte du commentaire
    likes = models.IntegerField(default=0)  # Champ pour stocker le nombre de J'aime
    created_at = models.DateTimeField(auto_now_add=True)  # Date de création du commentaire

    def __str__(self):
        return f"Commentaire de {self.user.username}"
