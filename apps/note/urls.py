from django.urls import path

from note import views

urlpatterns = [
    # main
    path('', views.main, name='main'),

    # group
    path('create-group/', views.GroupCreateView.as_view(), name='create_group'),

    # note
    path('note/', views.NoteListView.as_view(), name='note'),
    path('note/<int:pk>/', views.NoteDetailView.as_view(), name='note-detail'),
    path('note/<int:pk>/delete/', views.note_delete, name='note_delete'),
]
