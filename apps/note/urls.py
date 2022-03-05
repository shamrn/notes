from django.urls import path

from note.views import main, NoteListView, NoteDetailView, note_delete

urlpatterns = [
    path('', main, name='main'),
    path('note/', NoteListView.as_view(), name='note'),
    path('note/<int:pk>/', NoteDetailView.as_view(), name='note-detail'),
    path('note/<int:pk>/delete/', note_delete, name='note_delete')
]
