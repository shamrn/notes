from django.urls import path

from note.views import main, NoteListView

urlpatterns = [
    path('', main, name='main'),
    path('note/', NoteListView.as_view(), name='note')
]
