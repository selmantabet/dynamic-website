from flask import render_template, url_for, request, redirect, flash, session
from blog import app
from blog.forms import RegistrationForm, LoginForm
from flask_login import login_user, logout_user, current_user, login_required
import json

# https://roytuts.com/upload-and-display-image-using-python-flask/


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]


@app.route("/")
@app.route("/home")  # Main portfolio page, with all admin posts showing up.
def home():
    from blog.models import Post, User
    admin = User.query.filter_by(username="admin").first()
    posts = Post.query.filter_by(author_id=admin.id).all()
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


# Full display of a single post (with comments)
@app.route("/post/<int:post_id>")
def post(post_id):
    from blog.models import Post, Comment
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_id=post_id).all()
    return render_template('post.html', post=post, comments=comments)


@app.route("/user/<int:user_id>")
def user(user_id):
    from blog.models import Post, User
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(author_id=user_id).all()
    return render_template('user.html', user=user, posts=posts)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        from blog.models import User
        user = User(username=form.username.data, password=form.password.data)
        from blog import db
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!')
        return redirect(url_for('registered'))
    return render_template('register.html', title='Register', form=form)


@app.route("/registered")
def registered():
    return render_template('registered.html', title='Thanks!')


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
    # flash('You are now logged out. Thanks for your visit!')
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='My Account')


@app.route("/create", methods=['GET', 'POST'])
@login_required
def create():
    return render_template('create.html', title='Create Post')


@app.route("/toggle_mode")
def toggle_mode():
    session['mode'] = 'dark' if session.get('mode') == 'light' else 'light'
    if current_user.is_authenticated:
        settings = json.loads(current_user.settings_json)
        settings['mode'] = session['mode']
        current_user.settings_json = json.dumps(settings)
        from blog import db
        db.session.commit()
    return redirect(url_for('home'))


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")


def settings_updater():
    settings = json.loads(current_user.settings_json)
    settings['mode'] = session['mode']
    current_user.settings_json = json.dumps(settings)
    from blog import db
    db.session.commit()
    return


def settings_loader(settings_json):
    settings = json.loads(settings_json)
    session.update(settings)
    return
