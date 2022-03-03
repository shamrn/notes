from django.conf import settings
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
    """Note Base View"""

    model = Note

    def get_queryset(self):
        return (super().get_queryset()  # NOQA
                       .by_user(self.request.user)  # NOQA
                       .select_related_group()
                       .order_by('-date_created'))


class NoteListView(NoteBaseView, FilterView):
    """Note list view"""

    template_name = 'note/main_note.html'
    context_object_name = 'notes'
    paginate_by = 30
    filterset_class = NoteFilterSet

    def get_context_data(self, *, object_list=None, **kwargs):
        """Added in context - list of user groups"""

        context = super(NoteListView, self).get_context_data(**kwargs)
        context.update({'groups': Group.objects.filter(user=self.request.user)})
        return context


class NoteDetailView(NoteBaseView, DetailView):
    """Note detail view """

    template_name = 'note/detail_note.html'
    context_object_name = 'note'
