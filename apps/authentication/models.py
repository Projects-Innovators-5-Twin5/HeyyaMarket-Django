from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    
    VENDEUR = 'VENDEUR'
    CLIENT = 'CLIENT'

    ROLE_CHOICES = (
        (VENDEUR, 'Vendeur'),
        (CLIENT, 'Client'),
    )

    role = models.CharField(max_length=30, choices=ROLE_CHOICES, verbose_name='Rôle')
