# apps/reviews/admin.py

from django.contrib import admin
from .models import Avis, Commentaire

admin.site.register(Avis)
admin.site.register(Commentaire)
