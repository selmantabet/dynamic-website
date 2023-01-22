"""
Database Creation Script

Developed by Selman Tabet @ https://selman.io/
------------------------------------------------
Developed for Coursework 2 of the CMT120 course at Cardiff University

This script should only be used for first-time setup
and the environment variables should be set in the base.env file in the blog/env folder.

Database address is based on the database instance associated with this project, which
is set up using a separate set of environment variables using the blog/config/cfg.py script.
"""
# Initilaize the Flask app
from blog import app, db

# Initialize models
from blog.models import User
import time
import os
import json
from dotenv import load_dotenv
import datetime

cwd = os.getcwd()
base_env_path = os.path.join(cwd, "blog", "env", "base.env")
print("base env path: ", base_env_path)
if (os.path.exists(base_env_path)):
    load_dotenv(dotenv_path=base_env_path)
    print("base env vars initialized from db_creation")

# Initialize models
with app.app_context():
    input("Press Enter to create the database..")
    db.create_all()

    try:
        admin = User(username="admin", password=os.environ.get("ADMIN_PASSWORD"), creation_date=datetime.datetime(2023, 1, 15, 18, 0, 0),
                     settings_json=json.dumps({"has_avatar": False, "mode": "dark"}))
        user = User(username="user", password=os.environ.get("ADMIN_PASSWORD"),
                    settings_json=json.dumps({"has_avatar": False, "mode": "dark"}))
    except AttributeError:  # If ADMIN_PASSWORD was not set, prompt the user to enter the password
        pw = input("Enter admin password: ")
        admin = User(username="admin", password=pw, settings_json=json.dumps(
            {"has_avatar": False, "mode": "dark"}))
        user = User(username="user", password=pw, settings_json=json.dumps(
            {"has_avatar": False, "mode": "dark"}))

    users = [admin, user]

    for i in users:
        db.session.add(i)
        time.sleep(0.2)

    db.session.commit()
print("Database created.")
