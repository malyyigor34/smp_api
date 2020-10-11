from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_url(value: str):
    if value.find('.') == -1:
        raise ValidationError(
            (f'{value} is not correct url')
        )
