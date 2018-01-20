from django import forms

from .models import Profile

class AboutDaniel(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['biography', 'display']
