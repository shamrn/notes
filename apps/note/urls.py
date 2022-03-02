from django.contrib.auth import views as auth_views
from django.urls import path
from note.views import main, main_note
from django.views.generic import TemplateView

urlpatterns = [
    path('', main, name='main'),
    path('note/', main_note, name='note')
]
