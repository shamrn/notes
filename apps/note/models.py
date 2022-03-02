from django.db import models


class Group(models.Model):
    """Model group note"""

    name = models.CharField('Название', max_length=100)


class Note(models.Model):
    """Model note"""

    name = models.CharField('Название', max_length=100)
    group = models.OneToOneField(Group, on_delete=models.SET_NULL,
                                 blank=True, null=True, verbose_name='Группа')
    description = models.TextField('Текст заметки')
    date_created = models.DateTimeField('Дата создания', auto_now_add=True)

    # removal
    await_removal = models.BooleanField(default=False)
    date_removed = models.DateTimeField('Дата удаления', null=True, blank=True)
