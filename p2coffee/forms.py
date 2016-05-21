from django import forms
from p2coffee.models import SensorEvent


class SensorEventForm(forms.ModelForm):
    class Meta:
        model = SensorEvent
        fields = ['name', 'value', 'id']


class SlackOutgoingForm(forms.Form):
    token = forms.CharField(required=True)
    team_id = forms.CharField(required=True)
    team_domain = forms.CharField(required=True)
    channel_id = forms.CharField(required=True)
    channel_name = forms.CharField(required=True)
    timestamp = forms.CharField(required=True)
    user_id = forms.CharField(required=True)
    user_name = forms.CharField(required=True)
    text = forms.CharField(required=True)
    trigger_word = forms.CharField(required=True)