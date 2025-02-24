from django import forms

from accounts.models import Shopper

class UserForm(forms.ModelForm):
    # Form for user registration
    class Meta:
        model = Shopper
        fields = ['first_name', 'last_name', 'email', 'password']
        # Password field is hidden
        widgets = {
            'password': forms.PasswordInput()
        }