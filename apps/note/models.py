from datetime import datetime, timedelta
from typing import Union

from django.conf import settings
from django.db import models
from django.http import request

from account.models import User
from extensions.filters import greatest_trigram_similarity


class GroupQuerySet(models.QuerySet):
    """Query set for model note"""

    def by_user(self, user: 'User') -> Union['GroupQuerySet', models.QuerySet]:
        """Filter by user"""

        return self.filter(user=user)


class Group(models.Model):
    """Model group note"""

    # Group for deleted notes
    deleted_number = -1
    deleted_label = 'Удаленные'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField('Название', max_length=100)

    objects = models.Manager.from_queryset(GroupQuerySet)()

    def __str__(self):
        return self.name

    @classmethod
    def bulk_update_name(cls, queryset: 'models.QuerySet', data: 'request.QueryDict'):
        """Update name for groups"""

        for group in queryset:
            group.name = data[str(group.id)]

        cls.objects.bulk_update(queryset, fields=['name'])


class NoteQuerySet(models.QuerySet):
    """Query set for model note"""

    def by_user(self, user: 'User') -> Union['NoteQuerySet', models.QuerySet]:
        """Filter by user"""

        return self.filter(user=user)

    def by_await_removal(self) -> Union['NoteQuerySet', models.QuerySet]:
        """Filter by await removal"""

        return self.filter(await_removal=True)

    def by_group(self, group_id: int) -> Union['NoteQuerySet', models.QuerySet]:
        """Filter by group"""

        if group_id == Group.deleted_number:
            return self.by_await_removal()

        return self.filter(group=group_id)

    def by_past_date_deletion(self) -> Union['NoteQuerySet', models.QuerySet]:
        """Check the note for the deletion date and return the queryset for deletion"""

        return self.by_await_removal().filter(date_removed__lte=datetime.now())

    def annotate_trigram_similarity(self, value: str) -> Union['NoteQuerySet', models.QuerySet]:
        """Trigram similarity for field 'name' and 'description'"""

        return self.annotate(
            trigram_similarity=greatest_trigram_similarity(
                fields=['name', 'description'], value=value
            ))


class Note(models.Model):
    """Model note"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField('Название', max_length=50)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL,
                              blank=True, null=True, verbose_name='Группа')
    description = models.TextField('Текст заметки')
    date_created = models.DateTimeField('Дата создания', auto_now_add=True)

    # removal
    await_removal = models.BooleanField(default=False)
    date_removed = models.DateTimeField('Дата удаления', null=True, blank=True)

    objects = models.Manager.from_queryset(NoteQuerySet)()

    def __str__(self):
        return self.name

    def set_await_removal(self):
        """Set await removal note"""

        if not self.await_removal:
            self.date_removed = datetime.now() + timedelta(days=settings.DAYS_BEFORE_REMOVAL)
            self.await_removal = True
            self.save(update_fields=['await_removal', 'date_removed'])

    def restore(self):
        """Restore with await removal note"""

        if self.await_removal:
            self.date_removed = None
            self.await_removal = False
            self.save(update_fields=['await_removal', 'date_removed'])
