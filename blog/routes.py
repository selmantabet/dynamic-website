from flask import render_template, url_for, request, redirect, flash
from blog import app
from blog.forms import RegistrationForm, LoginForm
from flask_login import login_user, logout_user, current_user, login_required


@app.route("/")
@app.route("/home")
def home():
    from blog.models import Post
    posts = Post.query.all()
    return render_template('home.html', posts=posts, current_user=current_user)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/post/<int:post_id>")
def post(post_id):
    from blog.models import Post
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


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
    return render_template('account.html', title='Account Settings')


@app.route("/create")
@login_required
def create():
    return render_template('create.html', title='Create Post')
