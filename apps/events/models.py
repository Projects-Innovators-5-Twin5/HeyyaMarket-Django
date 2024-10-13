from django.db import models
from django.conf import settings  # Pour utiliser AUTH_USER_MODEL
from django.contrib.auth.models import User

from django.db import models

class Event(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('finished', 'Finished'),
        ('cancelled', 'Cancelled'),
    ]

    EVENT_TYPE_CHOICES = [
    ('workshop', 'Workshop'),
    ('seminar', 'Seminar'),
    ('bootcamp', 'Bootcamp'),
    ('conference', 'Conference'),
    ('bazaar', 'Bazaar'),  # Adding a bazaar for local product showcases
    ('networking', 'Networking'),  # Adding networking events for entrepreneurs
    ]

    TARGET_AUDIENCE_CHOICES = [
        ('artisans_and_craftswomen', 'Artisans and Craftswomen'),
        ('aspiring_entrepreneurs', 'Aspiring Entrepreneurs'),
        ('small_business_owners', 'Small Business Owners'),
        ('students_and_young_professionals', 'Students and Young Professionals'),
        ('community_leaders_and_activists', 'Community Leaders and Activists'),
        ('hobbyists_and_creatives', 'Hobbyists and Creatives'),
        ('mentors_and_educators', 'Mentors and Educators'),
        ('nonprofit_organizations', 'Nonprofit Organizations and NGOs'),
    ]

    EVENT_THEME_CHOICES = [
        ('empowerment', 'Empowerment'),
        ('entrepreneurship', 'Entrepreneurship'),
        ('marketing', 'Marketing'),
        ('craftsmanship', 'Craftsmanship'),
        ('digital_skills', 'Digital Skills'),
    ]

    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    location = models.CharField(max_length=255)
    available_slots = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='scheduled')
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    event_type = models.TextField(blank=True)
    target_audience = models.TextField(blank=True)
    event_theme = models.TextField(blank=True)
    level = models.TextField(blank=True)

    def __str__(self):
        return self.title

    def get_event_types(self):
        return self.event_type.split(',') if self.event_type else []

    def get_target_audiences(self):
        return self.target_audience.split(',') if self.target_audience else []

    def get_event_themes(self):
        return self.event_theme.split(',') if self.event_theme else []

    def get_levels(self):
        return self.level.split(',') if self.level else []



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
    rating = models.PositiveIntegerField(null=True, blank=True, choices=[(i, str(i)) for i in range(1, 6)])  # Rating from 1 to 5

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f'{self.user} - {self.event.title} - {self.get_status_display()}'
