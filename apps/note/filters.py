import django_filters as filters

from extensions.validators import empty_value
from note.models import Group


class NoteFilterSet(filters.FilterSet):
    """Filter set for note"""

    group = filters.CharFilter(method='by_group')
    search = filters.CharFilter(method='by_trigram_similarity')
    order = filters.OrderingFilter(fields=['date_created'])

    @staticmethod
    def by_group(queryset, name: str, value: str):  # NOQA
        """Filter by group and include group - deleted"""

        if (empty_value(value) and value.isnumeric() or
                (hasattr(Group, 'deleted_number') and value == str(Group.deleted_number))):
            return queryset.by_group(int(value))
        return queryset.none()

    @staticmethod
    def by_trigram_similarity(queryset, name: str, value: str):  # NOQA
        """Trigram similarity for notes"""

        if empty_value(value):
            return queryset.annotate_trigram_similarity(value).filter(trigram_similarity__gt=0.3)
        return queryset.none()
