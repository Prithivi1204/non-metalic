from django import forms
from .models import UserProfile


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_pic']
        # Styling kaga widgets sethukalaam
        widgets = {
            'profile_pic': forms.FileInput(attrs={'class': 'form-control bg-dark text-white border-secondary'})
        }
