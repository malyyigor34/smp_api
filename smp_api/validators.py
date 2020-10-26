from django.core.exceptions import ValidationError


def validate_url(value: str):
    if value.find('.') == -1:
        raise ValidationError(
            (f'{value} is not correct url')
        )
