from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = '4cf37f8b7ab4708d7a9f9ac5aed3d2aa0e'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db'

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_maneger = LoginManager(app)
login_maneger.login_view = 'login'
login_maneger.login_message_category = 'alert-info'

from comunidade_impressionadora import routes