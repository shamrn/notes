from django import forms

from extensions.forms import BaseFormMixin
from note.models import Group, Note


class GroupCreateForm(BaseFormMixin, forms.ModelForm):
    """Group create form"""

    class Meta:
        model = Group
        fields = ['name']


class NoteCreateForm(BaseFormMixin, forms.ModelForm):
    """Note create form"""

    class Meta:
        model = Note
        fields = ['name', 'group', 'description']
