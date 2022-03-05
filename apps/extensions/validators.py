
# These values, if given to validate(), will trigger the self.required check.
EMPTY_VALUES = (None, '', [], (), {})


def empty_value(value):
    """Check for empty value"""

    return bool(value not in EMPTY_VALUES)
