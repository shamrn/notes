import django_filters as filters
from note.models import Note
from extension.validators import EMPTY_VALUES


class NoteFilterSet(filters.FilterSet):
    """Filter set for note"""

    search = filters.CharFilter(method='by_trigram_similarity')

    class Meta:
        model = Note
        fields = ['date_created']

    @staticmethod
    def by_trigram_similarity(queryset, name: str, value: str):

        if value not in EMPTY_VALUES:
            return queryset.annotate_trigram_similarity(value).filter(trigram_similarity__gt=0.3)
        return queryset.none()
