from flask import jsonify, render_template

from . import app


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


class InvalidAPIUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        return dict(message=self.message)


class UrlmapCreationErrorAPI(InvalidAPIUsage):
    pass


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(UrlmapCreationErrorAPI)
def invalid_api_usage(error):
    return jsonify(error.to_dict()), error.status_code