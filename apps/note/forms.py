from django import forms

from extensions.forms import BaseFormMixin
from note.models import Group, Note


class GroupCreateForm(BaseFormMixin, forms.ModelForm):
    """Group create form"""

    class Meta:
        model = Group
        fields = ['name']


class GroupsUpdateForm(forms.Form):
    """Groups update form"""

    def __init__(self, queryset,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queryset = queryset

        self._make_fields()

    def _make_fields(self):
        name_field = Group.name.field

        for note in self.queryset:
            field = forms.CharField()
            field.widget.attrs.update({
                'class': 'form-field',
                'value': note.name,
                'max_length': name_field.max_length,
                'placeholder': name_field.verbose_name,
            })
            self.fields[str(note.id)] = field


class NoteCreateForm(BaseFormMixin, forms.ModelForm):
    """Note create form"""

    class Meta:
        model = Note
        fields = ['name', 'group', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].widget.attrs.update({'class': 'form-field form-field-desc', })


class NoteUpdateForm(NoteCreateForm):
    """Note update form"""
