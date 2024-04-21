"""
Helper functions for user settings. Includes upload scopes and session management.

Developed by Selman Tabet @ https://selman.io/
------------------------------------------------
Developed for Coursework 2 of the CMT120 course at Cardiff University
"""
from blog import app, db
from flask import session
from flask_login import current_user
from flask_uploads import UploadSet, configure_uploads, IMAGES
import json
import os

# File uploads based on https://flask-uploads.readthedocs.io/en/latest/
images = UploadSet('images', IMAGES)


def settings_updater():
    settings = json.loads(current_user.settings_json)
    if session.get("mode") is None:
        session['mode'] = 'light'
    settings['mode'] = session['mode']
    current_user.settings_json = json.dumps(settings)
    db.session.commit()
    return


def settings_loader(settings_json):
    settings = json.loads(settings_json)
    session.update(settings)
    upload_dir = app.config["DEFAULT_UPLOAD_DEST"]
    user_dir = os.path.join(upload_dir, str(current_user.id))
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)
    app.config["UPLOADED_IMAGES_DEST"] = user_dir
    # Reconfigure uploads to use the user's upload directory
    configure_uploads(app, images)
    return


def settings_clearer():
    mode = session.get('mode')
    session.clear()
    session['mode'] = mode  # Retain mode to not "flashbang" the user xDDDDD
    app.config["UPLOADED_IMAGES_DEST"] = app.config["DEFAULT_UPLOAD_DEST"]
    return


def reset_user_settings(user):
    settings = json.loads(user.settings_json)
    defaults = {
        "has_avatar": False,
        "mode": "light"
    }
    settings.update(defaults)
    user.settings_json = json.dumps(settings)
    db.session.commit()
    return
