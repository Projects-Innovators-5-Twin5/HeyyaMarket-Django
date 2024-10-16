from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    VENDEUR = 'VENDEUR'
    CLIENT = 'CLIENT'
    ADMIN = 'ADMIN'

    ROLE_CHOICES = (
        (VENDEUR, 'Vendeur'),
        (CLIENT, 'Client'),
        (ADMIN , 'Admin')
    )
    profile_photo = models.ImageField(verbose_name='Photo de profil',default='default.jpg', blank=True)
    bio = models.CharField(max_length=255, blank=True, null=True)
    addresse = models.CharField(max_length=255, blank=True, null=True)
    tel = models.CharField(max_length=8, blank=True, null=True)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, verbose_name='Rôle')
    brand_name = models.CharField(max_length=255, blank=True, null=True)
    brand_description = models.TextField(blank=True, null=True)
    brand_email = models.EmailField(blank=True, null=True)
    brand_rne_number = models.PositiveIntegerField(null=True, blank=True, verbose_name='RNE Number')
    brand_logo = models.ImageField(upload_to='brand_logos/', blank=True, null=True)
    request_status = models.CharField(max_length=10, blank=True, null=True)
