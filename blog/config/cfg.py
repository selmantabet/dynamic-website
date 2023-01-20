"""
Config Script - Loaded upon app initialization

Developed by Selman Tabet @ https://selman.io/
------------------------------------------------
Developed for Coursework 2 of the CMT120 course at Cardiff University

Based on a config script that I developed during my time as the architect
of the Shopify Integration Gateway at Snoonu Qatar's fleet management system (FalconFlex)
"""
from dotenv import load_dotenv
import os

cwd = os.getcwd()
base_env_path = os.path.join(cwd, "blog", "env", "base.env")
print("base env path: ", base_env_path)
if (os.path.exists(base_env_path)):
    load_dotenv(dotenv_path=base_env_path)
    print("base env vars initialized from config")

DEFAULT_UPLOAD_DEST = os.path.join(cwd, "blog", "static", "uploads")
UPLOADED_IMAGES_DEST = os.path.join(cwd, "blog", "static", "uploads")
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

SQLALCHEMY_TRACK_MODIFICATIONS = False  # Suppresses SQLAlchemy warnings

# Load the dev env vars anyway, for now
dev_env_path = os.path.join(cwd, "blog", "env", "dev.env")
print("dev env path: ", dev_env_path)
if (os.path.exists(dev_env_path)):
    load_dotenv(dotenv_path=dev_env_path)
    print("dev env vars initialized from config")

if os.environ.get("ENV_TYPE") == "OPENSHIFT" or os.environ.get("ENV_TYPE") == "STAGING":
    if os.environ["ENV_TYPE"] == "STAGING":
        print("Staging deployment detected.")
    else:
        print("OpenShift deployment detected.")
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
        dbuser=os.environ["MYSQL_USER"],
        dbpass=os.environ["MYSQL_PASSWORD"],
        dbhost=os.environ["MYSQL_ADDRESS"],
        dbname=os.environ["MYSQL_DB_NAME"]
    )
else:
    if os.environ.get("ENV_TYPE") == "DEV":
        staging_env_path = os.path.join(cwd, "blog", "env", "staging.env")
        print("staging env path: ", staging_env_path)
        if (os.path.exists(staging_env_path)):
            load_dotenv(dotenv_path=staging_env_path)
            print("staging env vars initialized from config")
    elif os.environ.get("ENV_TYPE") == "PROD":
        prod_env_path = os.path.join(cwd, "blog", "env", "prod.env")
        print("prod env path: ", prod_env_path)
        if (os.path.exists(prod_env_path)):
            load_dotenv(dotenv_path=prod_env_path)
        print("prod env vars initialized from config")
        SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
            dbuser=os.environ["MYSQL_USER"],
            dbpass=os.environ["MYSQL_PASSWORD"],
            dbhost=os.environ["MYSQL_ADDRESS"],
            dbname=os.environ["MYSQL_DB_NAME"]
        )
    else:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
            os.path.join(cwd, "blog", 'blog_dev.db')
