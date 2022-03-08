from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import DetailView, CreateView, UpdateView
from django_filters.views import FilterView

from note.filters import NoteFilterSet
from note.forms import GroupCreateForm, NoteCreateForm, GroupsUpdateForm
from note.models import Group, Note
from django.urls import reverse_lazy


def main(request):
    """Main page view"""

    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)

    return render(request, template_name='main.html')


class GroupCreateView(LoginRequiredMixin, CreateView):
    """Group create view"""

    model = Group
    template_name = 'note/create_group.html'
    form_class = GroupCreateForm
    success_url = reverse_lazy('note')

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        return super(GroupCreateView, self).form_valid(form)


@login_required
def groups_update(request):
    """Update groups. We get a list of changed groups as input"""

    queryset = Group.objects.by_user(request.user)

    if request.method == 'POST':
        Group.bulk_update_name(queryset=queryset, data=request.POST)  # TODO

        return redirect('note')

    form = GroupsUpdateForm(queryset)
    return render(request=request, template_name='note/update_group.html', context={'form': form})


class NoteBaseView(LoginRequiredMixin):
    """Note base view"""

    model = Note

    def get_queryset(self):
        return (super().get_queryset()  # NOQA
                .by_user(self.request.user)  # NOQA
                .filter(await_removal=False)
                .select_related_group()
                .order_by('-date_created'))


class NoteListView(NoteBaseView, FilterView):
    """Note list view"""

    template_name = 'note/main_note.html'
    context_object_name = 'notes'
    paginate_by = 20
    filterset_class = NoteFilterSet

    def get_context_data(self, *, object_list=None, **kwargs):
        """Added in context - list of user groups"""

        context = super(NoteListView, self).get_context_data(**kwargs)
        context.update(
            {
                'groups': Group.objects.by_user(self.request.user),
                'group_deleted_label': Group.deleted_label,
                'group_deleted_number': Group.deleted_number,
                'quantity_notes': 234325,  # TODO перехватить django запрос?
             }
        )
        return context


class NoteDetailView(NoteBaseView, DetailView):  # TODO or UpdateView?
    """Note detail view"""

    template_name = 'note/detail_note.html'
    context_object_name = 'note'


@login_required
def note_delete(request, pk):  # TODO no work
    """Set note for await removal"""

    if note := Note.objects.filter(pk=pk).by_user(request.user).first():  # NOQA
        note.set_await_removal()

    return redirect('note')


class NoteCreateView(NoteBaseView, CreateView):
    """Create note view"""

    model = Note
    template_name = 'note/create_note.html'
    form_class = NoteCreateForm
    success_url = reverse_lazy('note')

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        return super(NoteCreateView, self).form_valid(form)
