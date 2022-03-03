from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm

from account.models import User


class BaseAuthorizationForm:
    """Base user form"""

    class Meta:
        model = User

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:  # NOQA
            self.fields[field].widget.attrs.update(  # NOQA
                {
                    'class': 'form-field',
                    'placeholder': f"{self.fields[f'{field}'].label}"  # NOQA
                }
            )


class SignUpForm(BaseAuthorizationForm, UserCreationForm):
    """Form for sign up user"""

    class Meta(BaseAuthorizationForm.Meta):
        fields = ['email']


class SignInForm(BaseAuthorizationForm, AuthenticationForm):
    """Form for sign in user"""
