from django import forms
from django.contrib.auth.forms import AuthenticationForm


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Username',
                'class': 'form-control'
            }
        ),
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'new-password',
                'placeholder': 'Password',
                'class': 'form-control'
            }
        ),
    )
