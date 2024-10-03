import os
import string


class Configs(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')


PATTERN_SHORT_FIELD = r'^[a-zA-Z0-9]{1,16}$'
MIN_LENGTH_FIELD = 1
MAX_LENGTH_ORIGINAL = 1024
MAX_LENGTH_SHORT = 16
GEN_SHORT_LENGTH = 6
SHORT_LINK_CHARACTERS = string.ascii_letters + string.digits
API_FIELD_ORIGINAL_LINK = 'url'
API_FIELD_SHORT_LINK = 'custom_id'
