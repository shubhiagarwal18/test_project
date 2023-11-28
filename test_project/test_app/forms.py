
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import *


class RegistrationForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in ['username', 'password1', 'password2']:
            self.fields[field_name].help_text = ''

class UserProfileForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'date_of_birth']  # Include fields from UserProfile model

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

        widgets = {
            'password': forms.PasswordInput(),
        }

        labels = {
            'password': 'Password',
        }

class CombinedForm(UserProfileForm, UserForm):
    pass
    
class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ['text']
        error_messages = {
            'text': {
                'required': 'Please enter your review.', 
            }
        }

    def clean_text(self):
        text = self.cleaned_data['text']
        return text





