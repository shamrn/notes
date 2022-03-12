from django.urls import path

from note import views

urlpatterns = [
    # main
    path('', views.main, name='main'),

    # group
    path('group/create/', views.GroupCreateView.as_view(), name='group-create'),
    path('groups/update/', views.groups_update, name='groups-update'),
    path('group/<int:pk>/delete', views.GroupDeleteView.as_view(), name='group-delete'),

    # note
    path('note/', views.NoteListView.as_view(), name='note'),
    path('note/<int:pk>/', views.NoteDetailUpdateView.as_view(), name='note-detail-update'),
    path('note/create/', views.NoteCreateView.as_view(), name='note-create'),
    path('note/<int:pk>/delete/', views.NoteDeleteView.as_view(), name='note-delete'),
    path('note/<int:pk>/restore/', views.restore_note, name='note-restore')
]
