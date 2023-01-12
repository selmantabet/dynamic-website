from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .config import cfg
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '64c81e139e3c113ecf8393abeaf83028196ca82e2acf2a3a'

# DB Connection changed to mysql
basedir = os.path.abspath(os.path.dirname(__file__))
app.config.from_object(cfg)
print("DB created at ", app.config['SQLALCHEMY_DATABASE_URI'])
# print("Tracking: ", app.config['SQLALCHEMY_TRACK_MODIFICATIONS'])
db = SQLAlchemy(app)
# with app.app_context():
#     db.create_all()

login_manager = LoginManager()
login_manager.login_view = 'login'  # Go here if accessed a restricted page
login_manager.init_app(app)
