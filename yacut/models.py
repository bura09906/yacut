import random
from datetime import datetime

from settings import (API_FIELD_ORIGINAL_LINK, API_FIELD_SHORT_LINK,
                      GEN_SHORT_LENGTH, MAX_LENGTH_ORIGINAL, MAX_LENGTH_SHORT,
                      SHORT_LINK_CHARACTERS)

from . import db
from .error_handlers import ErrorCreatingShortLink, InvalidShortError
from .validators import validate_short


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_LENGTH_ORIGINAL), nullable=False)
    short = db.Column(db.String(MAX_LENGTH_SHORT), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def save(self):
        if self.get_by_field_short(self.short):
            raise InvalidShortError(
                'Предложенный вариант короткой ссылки уже существует.'
            )

        validate_short(self.short)

        existing_urlmap = self.get_by_filed_original(self.original)
        if existing_urlmap:
            return existing_urlmap

        db.session.add(self)
        db.session.commit()
        return self

    @staticmethod
    def get_unique_short_id():
        short = ''.join(
            random.choices(SHORT_LINK_CHARACTERS, k=GEN_SHORT_LENGTH)
        )
        if URLMap.get_by_field_short(short):
            raise ErrorCreatingShortLink(
                'Возникла ошибка при создании короткой ссылки. '
                'Повторите попытку'
            )
        return short

    @classmethod
    def get_by_filed_original(cls, original):
        return cls.query.filter_by(original=original).first()

    @classmethod
    def get_by_field_short(cls, short):
        return cls.query.filter_by(short=short).first()

    def to_dict(self, host_url):
        return dict(
            url=self.original,
            short_link=f'{host_url}{self.short}'
        )

    @classmethod
    def from_dict(cls, data):
        if not data.get(API_FIELD_SHORT_LINK):
            data[API_FIELD_SHORT_LINK] = cls.get_unique_short_id()
        return cls(
            original=data[API_FIELD_ORIGINAL_LINK],
            short=data[API_FIELD_SHORT_LINK]
        )
