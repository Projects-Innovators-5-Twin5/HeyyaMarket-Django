from django.contrib import admin

# Register your models here.

from .models import Event, Participation

admin.site.register(Event)
admin.site.register(Participation)