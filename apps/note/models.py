from datetime import datetime, timedelta
from typing import Union

from django.db import models

from account.models import User
from extensions.filters import greatest_trigram_similarity


class Group(models.Model):
    """Model group note"""

    deleted = -1  # Group for deleted notes

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField('Название', unique=True, max_length=100)

    def __str__(self):
        return self.name


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

        if group_id == Group.deleted:
            return self.by_await_removal()

        return self.filter(group=group_id)

    def by_past_date_deletion(self) -> Union['NoteManager', models.QuerySet]:  # TODO
        """Check the note for the deletion date and return the queryset for deletion"""

        return self.by_await_removal().filter(date_removed__lte=datetime.now())

    def select_related_group(self) -> Union['NoteQuerySet', models.QuerySet]:
        """Join with model - group"""

        return self.select_related('group')

    def annotate_trigram_similarity(self, value: str) -> Union['NoteQuerySet', models.QuerySet]:
        """Trigram similarity for field 'name' and 'description'"""

        return self.annotate(
            trigram_similarity=greatest_trigram_similarity(
                fields=['name', 'description'], value=value
            ))


class NoteManager(models.Manager):
    """Manager for models note"""


class Note(models.Model):
    """Model note"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField('Название', max_length=100)
    group = models.OneToOneField(Group, on_delete=models.SET_NULL,
                                 blank=True, null=True, verbose_name='Группа')
    description = models.TextField('Текст заметки')
    date_created = models.DateTimeField('Дата создания', auto_now_add=True)

    # removal
    await_removal = models.BooleanField(default=False)
    date_removed = models.DateTimeField('Дата удаления', null=True, blank=True)

    objects = NoteManager.from_queryset(NoteQuerySet)()

    def __str__(self):
        return self.name

    def set_await_removal(self):  # TODO
        """Set await removal note"""

        self.date_removed = datetime.now() + timedelta(days=30)
        self.await_removal = True
        self.save(update_fields=['await_removal', 'date_removed'])
