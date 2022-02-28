from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


class UserLoginForm(AuthenticationForm):
    """Custom form for authentication"""

    class Meta:
        """Meta class"""

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
