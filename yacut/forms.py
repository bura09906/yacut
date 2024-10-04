from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional

from settings import MAX_LENGTH_ORIGINAL, MAX_LENGTH_SHORT, MIN_LENGTH_FIELD
from .validators import validate_custom_id


class URLForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[
            DataRequired(message='Обязательное поле'),
            Length(MIN_LENGTH_FIELD, MAX_LENGTH_ORIGINAL),
            URL(message='Предоставленная ссылка некорректна'),
        ]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки (Необязательно)',
        validators=[
            Length(MIN_LENGTH_FIELD, MAX_LENGTH_SHORT),
            Optional(),
            validate_custom_id,
        ]
    )
    submit = SubmitField('Создать')