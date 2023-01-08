from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .config import cfg
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '<insert your secret key here>'

# DB Connection changed to mysql
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://USERNAME:PASSWORD@csmysql.cs.cf.ac.uk:3306/USERNAME_DATABASE_NAME'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config.from_object(cfg)


db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
