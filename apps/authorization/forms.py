from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm

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
