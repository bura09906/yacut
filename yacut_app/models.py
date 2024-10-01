from datetime import datetime

from . import db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(1024), nullable=False)
    short = db.Column(db.String(16), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self, host_url):
        return dict(
            url=self.original,
            short_link=f'{host_url}{self.short}'
        )

    def from_dict(self, data):
        setattr(self, 'original', data['url'])
        setattr(self, 'short', data['custom_id'])