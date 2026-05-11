# accounts/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.core.exceptions import ValidationError
import re


class RegisterForm(UserCreationForm):

    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter Username'
        })
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter Email'
        })
    )

    role = forms.ChoiceField(
        choices=CustomUser.ROLE_CHOICES
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter Password'
        })
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm Password'
        })
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role',
                  'password1', 'password2']

    # USERNAME VALIDATION
    def clean_username(self):

        username = self.cleaned_data.get('username')

        if len(username) < 4:
            raise ValidationError(
                "Username must be at least 4 characters"
            )

        if not username.isalnum():
            raise ValidationError(
                "Username should contain only letters and numbers"
            )

        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError(
                "Username already exists"
            )

        return username

    # EMAIL VALIDATION
    def clean_email(self):

        email = self.cleaned_data.get('email')

        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError(
                "Email already registered"
            )

        return email

    # PASSWORD VALIDATION
    def clean_password1(self):

        password = self.cleaned_data.get('password1')

        if len(password) < 8:
            raise ValidationError(
                "Password must be at least 8 characters"
            )

        if not re.search(r'[A-Z]', password):
            raise ValidationError(
                "Password must contain one uppercase letter"
            )

        if not re.search(r'[a-z]', password):
            raise ValidationError(
                "Password must contain one lowercase letter"
            )

        if not re.search(r'[0-9]', password):
            raise ValidationError(
                "Password must contain one number"
            )

        if not re.search(r'[@$!%*?&]', password):
            raise ValidationError(
                "Password must contain one special character"
            )

        return password

    # CONFIRM PASSWORD VALIDATION
    def clean(self):

        cleaned_data = super().clean()

        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 != password2:
            raise ValidationError(
                "Passwords do not match"
            )

        return cleaned_data