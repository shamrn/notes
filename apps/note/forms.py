from django import forms

from extensions.forms import BaseFormMixin
from note.models import Group


class GroupCreateForm(BaseFormMixin, forms.ModelForm):
    """Base group form"""

    class Meta:
        model = Group
        fields = ['name']
