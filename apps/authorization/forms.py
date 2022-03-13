from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from account.models import User
from extensions.forms import BaseFormMixin


class BaseAuthorizationForm(BaseFormMixin):
    """Base user form"""

    class Meta:
        model = User


class SignUpForm(BaseAuthorizationForm, UserCreationForm):
    """Form for sign up user"""

    class Meta(BaseAuthorizationForm.Meta):
        fields = ['email']


class SignInForm(BaseAuthorizationForm, AuthenticationForm):
    """Form for sign in user"""

    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True}),
                             validators=[validate_email])

    def get_invalid_login_error(self):
        return ValidationError({'username': 'Пожалуйста, введите корректный email и пароль.'})
