from django import forms

from accounts.models import Shopper

class UserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'bg-blanc border border-gray-300 text-primary text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5'
        })
    )
    # Form for user registration
    class Meta:
        model = Shopper
        fields = ['first_name', 'last_name', 'email', 'password']
        # Password field is hidden
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'bg-blanc border border-gray-300 text-primary text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'bg-blanc border border-gray-300 text-primary text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'bg-blanc border border-gray-300 text-primary text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'bg-blanc border border-gray-300 text-primary text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5'
            })
        }