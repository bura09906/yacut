from flask import jsonify, request

from . import app, db
from .core import (check_exist_urlmap, check_short_link, get_unique_short_id,
                   validate_short_link)
from .error_handlers import InvalidAPIUsage
from .models import URLMap


@app.route('/api/id/', methods=['POST'])
def get_short_link():
    data = request.get_json(silent=True)
    host_url = request.host_url

    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')

    urlmap = check_exist_urlmap(data['url'])

    if not data.get('custom_id') and not urlmap:
        data['custom_id'] = get_unique_short_id()
    elif not data.get('custom_id') and urlmap:
        return jsonify(urlmap.to_dict(host_url)), 201
    elif check_short_link(data['custom_id']):
        raise InvalidAPIUsage(
            'Предложенный вариант короткой ссылки уже существует.'
        )

    if validate_short_link(data['custom_id']):
        urlmap = URLMap()
        urlmap.from_dict(data)
        db.session.add(urlmap)
        db.session.commit()
        return jsonify(urlmap.to_dict(host_url)), 201
    else:
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_link(short_id):
    urlmap = URLMap.query.filter_by(short=short_id).first()
    if urlmap is None:
        raise InvalidAPIUsage('Указанный id не найден', status_code=404)
    return jsonify({'url': urlmap.original}), 200