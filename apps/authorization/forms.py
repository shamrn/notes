from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm

from account.models import User


class BaseAuthorizationFormMixin:  # TODO
    """Base user form"""

    class Meta:
        model = User

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    'class': "form-field",
                    'placeholder': f"{self.fields[f'{field}'].label}"
                }
            )


class SignUpForm(BaseAuthorizationFormMixin, UserCreationForm):   # TODO
    """Form for sign up user"""

    class Meta(BaseAuthorizationFormMixin.Meta):
        fields = ['email']


class SignInForm(BaseAuthorizationFormMixin, AuthenticationForm):  # TODO
    """Form for sign in user"""
