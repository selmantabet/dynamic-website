"""
Initialization file for the blog app

Developed by Selman Tabet @ https://selman.io/
------------------------------------------------
Developed for Coursework 2 of the CMT120 course at Cardiff University
"""


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .config import cfg
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '64c81e139e3c113ecf8393abeaf83028196ca82e2acf2a3a'

app.config.from_object(cfg)
if os.environ.get("ENV_TYPE") == "PROD" or os.environ.get("ENV_TYPE") == "STAGING":
    print("App is connected to MySQL server: ",
          os.environ["MYSQL_DB_NAME"], " on ", os.environ["MYSQL_ADDRESS"])
else:
    print("DB connected to: ", app.config['SQLALCHEMY_DATABASE_URI'])
db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.login_view = 'login'  # Go here when accessing a restricted page
login_manager.init_app(app)
