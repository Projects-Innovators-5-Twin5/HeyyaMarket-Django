from django import forms
from .models import Event

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

    class Meta:
        model = Event
        fields = ['title', 'description', 'start_datetime', 'end_datetime', 'location', 'available_slots', 'status', 'image', 'event_type', 'target_audience', 'event_theme', 'level']
        widgets = {
            'start_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
