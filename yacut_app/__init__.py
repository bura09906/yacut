from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from settings import Configs

app = Flask(__name__)
app.config.from_object(Configs)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from . import api_views, error_handlers, views
