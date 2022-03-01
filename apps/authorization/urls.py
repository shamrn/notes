from django.contrib.auth import views as auth_views
from django.urls import path

from authorization.forms import SignInForm
from authorization.views import SignUpView

urlpatterns = [
    path('sign-in/', auth_views.LoginView.as_view(
       authentication_form=SignInForm, template_name='authorization/sign_in.html'), name='sign-in'),
    path('sign-up/', SignUpView.as_view(), name='sign-up'),
]
