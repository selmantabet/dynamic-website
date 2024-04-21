"""
Application Routes - Accounts

Developed by Selman Tabet @ https://selman.io/
------------------------------------------------
Developed for Coursework 2 of the CMT120 course at Cardiff University
"""

from flask import render_template, url_for, request, redirect, flash, session
from blog import app, db
from blog.forms import SettingsForm, Deactivation
from blog.models import Post, User
from flask_login import logout_user, current_user, login_required
from blog.utils.settings import *
import os
import json


# View user profile
@app.route("/user/<int:user_id>")
def user(user_id):
    session['current_page'] = url_for('user', user_id=user_id)
    user = User.query.get_or_404(user_id)
    user_settings = json.loads(user.settings_json)
    if user_settings["has_avatar"]:
        avatar = url_for('static', filename='uploads/' +
                         str(user.id) + '/avatar.jpg')
    else:
        avatar = url_for('static', filename='img/avatar.png')
        # Default avatar: https://pluspng.com/png-81874.html
    return render_template('user.html', user=user, posts=user.post, avatar=avatar, comments=user.comment)


# View user account settings
@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    session['current_page'] = url_for('account')
    settings_loader(current_user.settings_json)
    deactivation = Deactivation()
    user_settings = SettingsForm()
    avatar_state = session["has_avatar"]
    if "delete_avatar" in request.form:
        os.remove(os.path.join(app.config["DEFAULT_UPLOAD_DEST"], str(
            current_user.id), "avatar.jpg"))
        settings = json.loads(current_user.settings_json)
        settings['has_avatar'] = False
        current_user.settings_json = json.dumps(settings)
        db.session.commit()
        flash("Avatar deleted.")
        return redirect(url_for('account'))
    if ("deactivate" in request.form) and (deactivation.validate_on_submit()):
        return redirect(url_for('confirm_deactivate'))
    if ("update" in request.form) and (user_settings.validate_on_submit()):
        avatar_path = os.path.join(app.config["DEFAULT_UPLOAD_DEST"], str(
            current_user.id), "avatar.jpg")
        if os.path.isfile(avatar_path):
            os.remove(avatar_path)
        filename = images.save(user_settings.avatar.data, name="avatar.jpg")
        if filename is not None:
            settings = json.loads(current_user.settings_json)
            settings['has_avatar'] = True
            current_user.settings_json = json.dumps(settings)
            db.session.commit()
        else:
            flash("Upload failed.")
        flash('Avatar updated!')
        return redirect(url_for('account'))
    return render_template('account.html', title='My Account', deactivation=deactivation, user_settings=user_settings, avatar_state=avatar_state)


# Confirm account deactivation
@app.route("/confirm_deactivate", methods=['GET', 'POST'])
@login_required
def confirm_deactivate():
    session['current_page'] = url_for('confirm_deactivate')
    form = Deactivation()
    settings_loader(current_user.settings_json)
    if form.validate_on_submit():
        # Doesn't matter if we query by id since the username is already setup to be unique
        user = User.query.filter_by(username=current_user.username).first()
        db.session.delete(user)
        db.session.commit()
        import shutil
        upload_dir = app.config["DEFAULT_UPLOAD_DEST"]
        user_dir = os.path.join(upload_dir, str(current_user.id))
        shutil.rmtree(user_dir)
        logout_user()  # Ensure that the current_user is logged out
        flash('Account deactivated. Sorry to see you go :c')
        return redirect(url_for('home'))
    return render_template('confirm_deactivate.html', title='Confirm Deactivation', form=form)
