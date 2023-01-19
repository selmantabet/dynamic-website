"""
Application routes

Developed by Selman Tabet @ https://selman.io/
------------------------------------------------
Developed for Coursework 2 of the CMT120 course at Cardiff University
"""

from flask import render_template, url_for, request, redirect, flash, session
from blog import app
from blog.forms import RegistrationForm, LoginForm, SettingsForm, PostForm, CommentForm, Deactivation, PasswordChangeForm
from flask_login import login_user, logout_user, current_user, login_required
from blog.utils.settings import *
import os
import json


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]


@app.route("/")
@app.route("/home")  # Main portfolio page, with all admin posts showing up.
def home():
    from blog.models import User
    admin = User.query.filter_by(username="admin").first()
    avatar = url_for('static', filename='img/' + 'admin.jpg')
    return render_template('home.html', posts=admin.post, avatar=avatar)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


# Full display of a single post (with comments)
@app.route("/post/<int:post_id>", methods=['GET', 'POST'])
def post(post_id):
    from blog.models import Post, Comment
    post = Post.query.get_or_404(post_id)
    author_settings = json.loads(post.user.settings_json)
    if author_settings["has_avatar"]:
        avatar = url_for('static', filename='uploads/' +
                         str(post.user.id) + '/avatar.jpg')
    else:
        avatar = url_for('static', filename='img/avatar.png')
        # Default avatar: https://pluspng.com/png-81874.html
    avatars = []
    for comment in post.comments:
        user_settings = json.loads(comment.user.settings_json)
        if user_settings["has_avatar"]:
            avatar = url_for('static', filename='uploads/' +
                             str(comment.user.id) + '/avatar.jpg')
        else:
            avatar = url_for('static', filename='img/avatar.png')
            # Default avatar: https://pluspng.com/png-81874.html
        avatars.append(avatar)
    packed_comments = zip(post.comments, avatars)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(content=form.content.data,
                          post_id=post_id, author_id=current_user.id)
        from blog import db
        db.session.add(comment)
        db.session.commit()
        flash('Comment successful!')
        return redirect(url_for('post', post_id=post_id))
    return render_template('post.html', post=post, comments=packed_comments, form=form, avatar=avatar)


@app.route("/delete_post/<int:post_id>")
@login_required
def delete_post(post_id):
    from blog.models import Post
    post = Post.query.get_or_404(post_id)
    if post.author_id != current_user.id:
        flash("You cannot delete this post!")
        return redirect(url_for('post', post_id=post_id))
    from blog import db
    db.session.delete(post)
    db.session.commit()
    flash("Post deleted!")
    return redirect(url_for('home'))


@app.route("/delete_comment/<int:comment_id>")
@login_required
def delete_comment(comment_id):
    from blog.models import Comment
    comment = Comment.query.get_or_404(comment_id)
    post_id = comment.post.id
    if comment.author_id != current_user.id:
        flash("You cannot delete this comment!")
        return redirect(url_for('post', post_id=post_id))
    from blog import db
    db.session.delete(comment)
    db.session.commit()
    flash("Comment deleted!")
    return redirect(url_for('post', post_id=post_id))


@app.route("/user/<int:user_id>")
def user(user_id):
    from blog.models import Post, User
    user = User.query.get_or_404(user_id)
    user_settings = json.loads(user.settings_json)
    if user_settings["has_avatar"]:
        avatar = url_for('static', filename='uploads/' +
                         str(user.id) + '/avatar.jpg')
    else:
        avatar = url_for('static', filename='img/avatar.png')
        # Default avatar: https://pluspng.com/png-81874.html
    return render_template('user.html', user=user, posts=user.post, avatar=avatar, comments=user.comment)


@app.route("/register", methods=['GET', 'POST'])
def register():
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


@app.route("/change_password", methods=['GET', 'POST'])
@login_required
def change_password():
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


@app.route("/login", methods=['GET', 'POST'])
def login():
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


@app.route("/logout")
@login_required
def logout():
    flash(f'You have successfully logged out, {current_user.username}!')
    logout_user()
    settings_clearer()
    return redirect(url_for('home'))


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    settings_loader(current_user.settings_json)
    deactivation = Deactivation()
    user_settings = SettingsForm()
    avatar_state = session["has_avatar"]
    if "delete_avatar" in request.form:
        from blog.utils.settings import images
        os.remove(os.path.join(app.config["DEFAULT_UPLOAD_DEST"], str(
            current_user.id), "avatar.jpg"))
        settings = json.loads(current_user.settings_json)
        settings['has_avatar'] = False
        current_user.settings_json = json.dumps(settings)
        from blog import db
        db.session.commit()
        flash("Avatar deleted.")
        return redirect(url_for('account'))
    if ("deactivate" in request.form) and (deactivation.validate_on_submit()):
        return redirect(url_for('confirm_deactivate'))
    if ("update" in request.form) and (user_settings.validate_on_submit()):
        from blog.utils.settings import images
        avatar_path = os.path.join(app.config["DEFAULT_UPLOAD_DEST"], str(
            current_user.id), "avatar.jpg")
        if os.path.isfile(avatar_path):
            os.remove(avatar_path)
        filename = images.save(user_settings.avatar.data, name="avatar.jpg")
        if filename is not None:
            settings = json.loads(current_user.settings_json)
            settings['has_avatar'] = True
            current_user.settings_json = json.dumps(settings)
            from blog import db
            db.session.commit()
        else:
            flash("Upload failed.")
        flash('Settings updated!')
        return redirect(url_for('account'))
    return render_template('account.html', title='My Account', deactivation=deactivation, user_settings=user_settings, avatar_state=avatar_state)


@app.route("/create", methods=['GET', 'POST'])
@login_required
def create():
    settings_loader(current_user.settings_json)
    from blog.utils.settings import images
    form = PostForm()
    from blog.models import Post
    if form.validate_on_submit():
        if form.picture.data is not None:
            if not allowed_file(form.picture.data.filename):
                flash("File type not allowed")
        post = Post(title=form.title.data, content=form.content.data,
                    author_id=current_user.id)
        from blog import db
        db.session.add(post)
        db.session.commit()
        if (form.picture.data != '') and (form.picture.data is not None):
            posted = Post.query.filter_by(
                title=form.title.data, author_id=current_user.id).order_by(Post.id.desc()).first()  # Get the post that was just created
            import uuid
            uuid_string = str(uuid.uuid4())
            filename = images.save(form.picture.data, name=uuid_string)
            if filename is not None:
                posted.image_file = filename
                db.session.commit()
        flash('Post successful!')
        return redirect(url_for('post', post_id=post.id))
    return render_template('create.html', title='Create Post', form=form)


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
    return redirect(url_for('home'))


@app.route("/confirm_deactivate", methods=['GET', 'POST'])
@login_required
def confirm_deactivate():
    form = Deactivation()
    settings_loader(current_user.settings_json)
    if form.validate_on_submit():
        from blog.models import User
        # Doesn't matter if we query by id since the username is already setup to be unique
        user = User.query.filter_by(username=current_user.username).first()
        from blog import db
        db.session.delete(user)
        db.session.commit()
        import shutil
        upload_dir = app.config["DEFAULT_UPLOAD_DEST"]
        print("Upload dir:", upload_dir)
        user_dir = os.path.join(upload_dir, str(current_user.id))
        shutil.rmtree(user_dir)
        logout_user()  # Ensure that the current_user is logged out
        flash('Account deactivated. Sorry to see you go :c')
        return redirect(url_for('home'))
    return render_template('confirm_deactivate.html', title='Confirm Deactivation', form=form)


@app.route("/cv_download")
def cv_download():
    from flask import send_file
    return send_file('static/cv.pdf', as_attachment=True)


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")
