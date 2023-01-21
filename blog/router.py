"""
Application router

Developed by Selman Tabet @ https://selman.io/
------------------------------------------------
Developed for Coursework 2 of the CMT120 course at Cardiff University

Contains the routes to the main pages of the application.
All other pages are defined in their respective routes files under blog/routes.
"""

from flask import render_template, url_for, redirect, session
from blog import app
from flask_login import current_user
from blog.utils.settings import *
from blog.utils.errors import *
from blog.utils.formatting import *

import babel
import json
# Import all routes
from blog.routes.accounts import *
from blog.routes.auth import *
from blog.routes.comments import *
from blog.routes.posts import *


@app.route("/")
@app.route("/home")  # Main portfolio page, with all admin posts showing up.
def home():
    # The current_page session key will be used by the color mode toggler to return to the same page
    session['current_page'] = url_for('home')
    from blog.models import User
    admin = User.query.filter_by(username="admin").first()
    avatar = url_for('static', filename='img/' + 'admin.jpg')
    return render_template('home.html', posts=admin.post, avatar=avatar)


@app.route("/about")
def about():
    session['current_page'] = url_for('about')
    return render_template('about.html', title='About')


@app.route("/toggle_mode")
def toggle_mode():
    if session.get('mode') is None:
        session['mode'] = 'dark'
    else:
        session['mode'] = 'dark' if session.get('mode') == 'light' else 'light'
    if current_user.is_authenticated:
        settings = json.loads(current_user.settings_json)
        settings['mode'] = session['mode']
        current_user.settings_json = json.dumps(settings)
        from blog import db
        db.session.commit()
    return redirect(session['current_page'])


@app.route("/cv_download")
def cv_download():
    from flask import send_file
    return send_file('static/cv.pdf', as_attachment=True)
