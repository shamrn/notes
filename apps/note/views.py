from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView

from note.models import Note


def main(request):
    """Main page view"""

    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)

    return render(request, template_name='main.html')


class NoteBaseView(LoginRequiredMixin):
    """Note Base View"""

    model = Note

    def get_queryset(self):
        return super().get_queryset().by_user(self.request.user).select_related_group()  # NOQA


class NoteListView(NoteBaseView, ListView):
    """Note list view"""

    template_name = 'note/main_note.html'
    context_object_name = 'notes'
    paginate_by = 30


class NoteDetailView(NoteBaseView, DetailView):
    """Note detail view """

    template_name = 'note/detail_note.html'
    context_object_name = 'note'
