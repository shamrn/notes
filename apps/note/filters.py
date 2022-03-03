import django_filters as filters
from note.models import Group, Note
from extension.validators import EMPTY_VALUES


class NoteFilterSet(filters.FilterSet):
    """Filter set for note"""

    search = filters.CharFilter(method='by_trigram_similarity')

    class Meta:
        model = Note
        fields = ['group']

    # def filter_queryset(self, queryset):
    #     """Overridden method"""
    #
    #     # TODO no work (
    #     queryset = super().filter_queryset(queryset)
    #
    #     group = self.data.get('group', None)
    #     if group and group == Group.deleted:
    #         return queryset.by_delete()
    #
    #     return queryset


    @staticmethod
    def by_trigram_similarity(queryset, name: str, value: str):  # NOQA
        """Trigram similarity for notes"""

        if value not in EMPTY_VALUES:
            return queryset.annotate_trigram_similarity(value).filter(trigram_similarity__gt=0.3)
        return queryset.none()
