from django.urls import path
from authorization.views import test

urlpatterns = [
    path('test/', test),
]
