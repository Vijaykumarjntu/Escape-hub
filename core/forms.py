from django import forms
from .models import UserProfile

class RealSelfForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['inner_self', 'struggles', 'crazy_interests', 'what_i_hide', 'looking_for']
        widgets = {
            'inner_self': forms.Textarea(attrs={
                'rows': 4, 
                'placeholder': 'I pretend to be normal but...\nI actually think about...\nMy inner monologue never stops...'
            }),
            'struggles': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Society expects me to...\nMy family doesn\'t understand...\nI feel lonely when...'
            }),
            'crazy_interests': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': '3 AM Wikipedia dives\nObscure documentaries\nBuilding useless things\nCollecting...'
            }),
            'what_i_hide': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'I cry at parties\nI have 50 unfinished projects\nI don\'t want a "normal" life'
            }),
            'looking_for': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Someone who also hates small talk\nSomeone to watch weird films with\nSomeone who won\'t ask "where is this going"'
            }),
        }
        labels = {
            'inner_self': '🌑 what\'s actually inside? (be honest)',
            'struggles': '💔 what hurts? what do you hide from the world?',
            'crazy_interests': '🤪 what do you love that others don\'t get?',
            'what_i_hide': '🎭 what don\'t people know about you?',
            'looking_for': '🔍 what kind of human are you trying to find?'
        }