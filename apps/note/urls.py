from django.urls import path

from note.views import main, NoteListView, NoteDetailView

urlpatterns = [
    path('', main, name='main'),
    path('note/', NoteListView.as_view(), name='note'),
    path('note/<int:pk>/', NoteDetailView.as_view(), name='note-detail'),
]
