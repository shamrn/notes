from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import DetailView
from django_filters.views import FilterView

from note.filters import NoteFilterSet
from note.models import Group, Note


def main(request):
    """Main page view"""

    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)

    return render(request, template_name='main.html')


class NoteBaseView(LoginRequiredMixin):
    """Note base view"""

    model = Note

    def get_queryset(self):
        return (super().get_queryset()  # NOQA
                       .by_user(self.request.user)  # NOQA
                       .select_related_group()
                       .order_by('-date_created'))
                       # TODO убрать из общего списка удаленные заметки


class NoteListView(NoteBaseView, FilterView):
    """Note list view"""

    template_name = 'note/main_note.html'
    context_object_name = 'notes'
    paginate_by = 20
    filterset_class = NoteFilterSet

    def get_context_data(self, *, object_list=None, **kwargs):
        """Added in context - list of user groups"""

        context = super(NoteListView, self).get_context_data(**kwargs)
        context.update({'groups': Group.objects.by_user(self.request.user)})
        return context


class NoteDetailView(NoteBaseView, DetailView):  # TODO or UpdateView?
    """Note detail view"""

    template_name = 'note/detail_note.html'
    context_object_name = 'note'


@login_required
def note_delete(request, pk):
    """Set note for await removal"""

    if note := Note.objects.filter(pk=pk).by_user(request.user).first():  # NOQA
        note.set_await_removal()

    return redirect('note')
