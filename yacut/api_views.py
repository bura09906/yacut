from flask import jsonify, request

from settings import API_FIELD_ORIGINAL_LINK

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap


@app.route('/api/id/', methods=['POST'])
def get_short_link():
    data = request.get_json(silent=True)
    host_url = request.host_url

    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if API_FIELD_ORIGINAL_LINK not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')

    urlmap = URLMap.from_dict(data)
    created_urlmap = urlmap.save()
    return jsonify(created_urlmap.to_dict(host_url)), 201


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_link(short_id):
    urlmap = URLMap.get_by_field_short(short_id)
    if urlmap is None:
        raise InvalidAPIUsage('Указанный id не найден', status_code=404)
    return jsonify({API_FIELD_ORIGINAL_LINK: urlmap.original}), 200