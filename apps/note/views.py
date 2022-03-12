from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView
from django_filters.views import FilterView

from note.filters import NoteFilterSet
from note.forms import GroupCreateForm, NoteCreateForm, GroupsUpdateForm, NoteUpdateForm
from note.models import Group, Note


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
    """Bulk update for groups field is 'name' """

    queryset = Group.objects.by_user(request.user).order_by('pk')
    # order for zip, in template render 2 objects ( form and queryset )

    if request.method == 'POST':
        Group.bulk_update_name(queryset=queryset, data=request.POST)  # TODO

        return redirect('note')

    form = GroupsUpdateForm(queryset)
    context = {'united_data': zip(form, queryset)}
    return render(request=request, template_name='note/update_group.html', context=context)


class GroupDeleteView(LoginRequiredMixin, DeleteView):
    model = Group
    template_name = 'note/group_delete.html'
    success_url = reverse_lazy('note')


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
    filterset_class = NoteFilterSet

    def get_context_data(self, *, object_list=None, **kwargs):
        """Overridden method 'get_context_data' Added in context - list of user groups"""

        context = super(NoteListView, self).get_context_data(**kwargs)
        context.update(
            {
                'groups': Group.objects.by_user(self.request.user),
                'group_deleted_label': Group.deleted_label,
                'group_deleted_number': Group.deleted_number,
                'query_group_id': self.request.GET.get('group'),
                'current_url': self.current_url,
             }
        )
        return context

    @property
    def current_url(self) -> str:
        """Return the url with get parameters, for united filter"""

        required_filter_fields = ['group', 'search', 'order']

        if list(filter(lambda field: field not in self.filterset_class.get_filters().keys(),
                       required_filter_fields)):

            raise AttributeError(f'One of the required fields for filtering is missing,'
                                 f' the required filter fields: {required_filter_fields}')

        current_url = '/note/'
        full_path = self.request.get_full_path()

        if 'search' in full_path or 'group' in full_path:
            if full_path.count('order') >= 1:
                current_url = full_path.split('&')[0]
            else:
                current_url = full_path

        return current_url


class NoteCreateView(NoteBaseView, CreateView):
    """Create note view"""

    template_name = 'note/create_note.html'
    form_class = NoteCreateForm
    success_url = reverse_lazy('note')

    def form_valid(self, form):
        """Overridden method 'form_valid' to add a user to instance"""

        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        return super().form_valid(form)

    def get_form(self, *args, **kwargs):
        """Overridden method 'get_form' to sort groups by user"""

        form = super().get_form(*args, **kwargs)
        form.fields['group'].queryset = Group.objects.by_user(self.request.user)
        return form


class NoteDetailUpdateView(NoteCreateView, UpdateView):
    """Note detail update view"""

    template_name = 'note/detail_update_note.html'
    form_class = NoteUpdateForm


class NoteDeleteView(LoginRequiredMixin, DeleteView):
    model = Group
    template_name = 'note/note_delete.html'
    success_url = reverse_lazy('note')

@login_required
def note_delete(request, pk):  # TODO no work
    """Set note for await removal"""

    if note := Note.objects.filter(pk=pk).by_user(request.user).first():  # NOQA
        note.set_await_removal()

    return redirect('note')
