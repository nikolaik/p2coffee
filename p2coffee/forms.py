from django import forms
from p2coffee.models import LogEvent


class LogEventForm(forms.ModelForm):
    class Meta:
        model = LogEvent
        fields = ['name', 'value', 'id']
