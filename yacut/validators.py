import re

from wtforms.validators import ValidationError

from settings import PATTERN_SHORT_FIELD

from .error_handlers import InvalidShortError


def validate_short(short_link):
    if not re.fullmatch(PATTERN_SHORT_FIELD, short_link):
        raise InvalidShortError(
            'Указано недопустимое имя для короткой ссылки'
        )


def validate_custom_id(form, field):
    if not re.fullmatch(PATTERN_SHORT_FIELD, field.data):
        raise ValidationError('Указано недопустимое имя для короткой ссылки')
