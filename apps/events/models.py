from django.db import models
from django.conf import settings  # Pour utiliser AUTH_USER_MODEL
from django.contrib.auth.models import User

class Event(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('finished', 'Finished'),
        ('cancelled', 'Cancelled'),
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    location = models.CharField(max_length=255)
    available_slots = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='scheduled')
    image = models.ImageField(upload_to='events/', blank=True, null=True)  # Add this line for the image field

    def __str__(self):
        return self.title

class Participation(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('pending', 'Pending'),
        ('refused', 'Refused'),
        ('cancelled', 'Cancelled'),  # Added for cancellation
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    feedback = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f'{self.user} - {self.event.title} - {self.get_status_display()}'
