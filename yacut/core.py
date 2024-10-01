import random
import re
import string

from . import db
from .models import URLMap


def check_short_link(short_link):
    return db.session.query(URLMap.short).filter_by(
        short=short_link
    ).first() is not None


def check_exist_urlmap(original_link):
    return URLMap.query.filter_by(original=original_link).first()


def gen_random_string():
    return ''.join(
        random.choices(string.ascii_letters + string.digits, k=6)
    )


def get_unique_short_id():
    short_link = gen_random_string()
    while check_short_link(short_link):
        short_link = gen_random_string()
    return short_link


def validate_short_link(short_link):
    return re.fullmatch(r'^[a-zA-Z0-9]{1,16}$', short_link)
