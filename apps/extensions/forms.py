
class BaseFormMixin:
    """Base form mixin"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:  # NOQA
            self.fields[field].widget.attrs.update(  # NOQA
                {
                    'class': 'form-field',
                    'placeholder': f"{self.fields[f'{field}'].label}"  # NOQA
                }
            )
