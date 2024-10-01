from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional


class URLForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[
            DataRequired(message='Обязательное поле'),
            Length(1, 256),
            URL(message='Предоставленная ссылка некорректна'),
        ]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки (Необязательно)',
        validators=[Length(1, 16), Optional()]
    )
    submit = SubmitField('Создать')