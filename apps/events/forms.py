from django import forms
from .models import Event
from django.core.exceptions import ValidationError
from django.utils import timezone

class EventForm(forms.ModelForm):
    event_type = forms.MultipleChoiceField(
        choices=Event.EVENT_TYPE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    target_audience = forms.MultipleChoiceField(
        choices=Event.TARGET_AUDIENCE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    event_theme = forms.MultipleChoiceField(
        choices=Event.EVENT_THEME_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    level = forms.MultipleChoiceField(
        choices=Event.LEVEL_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    price = forms.IntegerField(required=False)  # Ensure price can be left empty


    class Meta:
        model = Event
        fields = ['title', 'description', 'start_datetime', 'end_datetime', 'location', 'available_slots', 'price' , 'status', 'image', 'event_type', 'target_audience', 'event_theme', 'level']
        widgets = {
            'start_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),

        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title:
            raise ValidationError("Event Title is required.")
        if len(title) < 5:
            raise ValidationError("Event Title must be at least 5 characters long.")
        return title

    def clean_location(self):
        location = self.cleaned_data.get('location')
        if not location:
            raise ValidationError("Location is required.")
        return location

    def clean_start_datetime(self):
        start_datetime = self.cleaned_data.get('start_datetime')
        if not start_datetime:
            raise ValidationError("Start Date & Time is required.")
        return start_datetime

    def clean_end_datetime(self):
        end_datetime = self.cleaned_data.get('end_datetime')
        start_datetime = self.cleaned_data.get('start_datetime')
        if not end_datetime:
            raise ValidationError("End Date & Time is required.")
        if start_datetime and end_datetime <= start_datetime:
            raise ValidationError("End Date & Time must be after Start Date & Time.")
        return end_datetime

    def clean_available_slots(self):
        available_slots = self.cleaned_data.get('available_slots')
        if available_slots is None:
            raise ValidationError("Available Slots are required.")
        if available_slots < 1:
            raise ValidationError("Available Slots must be at least 1.")
        return available_slots
