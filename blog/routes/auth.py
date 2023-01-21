"""
Application Routes - Authentication

Developed by Selman Tabet @ https://selman.io/
------------------------------------------------
Developed for Coursework 2 of the CMT120 course at Cardiff University
"""

from flask import render_template, url_for, request, redirect, flash, session
from blog import app
from blog.forms import RegistrationForm, LoginForm, PasswordChangeForm
from flask_login import login_user, logout_user, current_user, login_required
from blog.utils.settings import *
import json


# Signup page
@app.route("/register", methods=['GET', 'POST'])
def register():
    session['current_page'] = url_for('register')
    form = RegistrationForm()
    if form.validate_on_submit():
        from blog.models import User
        user = User(username=form.username.data, password=form.password.data,
                    settings_json=json.dumps({"has_avatar": False, "mode": session["mode"]}))
        from blog import db
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! You can now log in.')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


# Password change page
@app.route("/change_password", methods=['GET', 'POST'])
@login_required
def change_password():
    session['current_page'] = url_for('change_password')
    form = PasswordChangeForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.new_password.data
            from blog import db
            db.session.commit()
            flash('Password changed successfully!')
            return redirect(url_for('login'))
        else:
            flash('Old password is incorrect!')
    return render_template('change_password.html', title='Change Password', form=form)


# Login page
@app.route("/login", methods=['GET', 'POST'])
def login():
    session['current_page'] = url_for('login')
    form = LoginForm()
    if form.validate_on_submit():
        from blog.models import User
        user = User.query.filter_by(username=form.username.data).first()
        remember = True if request.form.get('remember') else False
        if user is not None and user.verify_password(form.password.data):
            login_user(user, remember=remember)
            # Load all settings to session
            settings_loader(current_user.settings_json)
            flash(f'You have successfully logged in, {current_user.username}!')
            return redirect(url_for('home'))
        flash('Invalid username or password.')
    return render_template('login.html', title='Login', form=form)


# Logout function
@app.route("/logout")
@login_required
def logout():
    flash(f'You have successfully logged out, {current_user.username}!')
    logout_user()
    return redirect(url_for('home'))
