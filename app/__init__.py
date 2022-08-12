import imp
from flask import Flask
from flask_moment import Moment
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
app.config['SECRET_KEY'] = '3cd0bf26f393b9c6b6f719c2be08a535'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

migrate = Migrate(app, db)

from app import routes, models