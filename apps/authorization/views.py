from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from account.models import User
from authorization.forms import SignUpForm


class SignUpView(SuccessMessageMixin, CreateView):
    """Create sign up view"""

    model = User
    form_class = SignUpForm
    success_message = 'Аккаунт успешно создан.'
    template_name = 'authorization/sign_up.html'
    success_url = reverse_lazy(settings.LOGIN_REDIRECT_URL)
