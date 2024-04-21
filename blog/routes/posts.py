"""
Application Routes - Posts

Developed by Selman Tabet @ https://selman.io/
------------------------------------------------
Developed for Coursework 2 of the CMT120 course at Cardiff University
"""

from flask import render_template, url_for, redirect, flash, session
from blog import app, db
from blog.forms import PostForm, CommentForm
from blog.models import Post, Comment
from flask_login import current_user, login_required
from blog.utils.settings import *
from blog.utils.files import *
import os
import json


# Full display of a single post (with comments)
@app.route("/post/<int:post_id>", methods=['GET', 'POST'])
def post(post_id):
    session['current_page'] = url_for('post', post_id=post_id)
    post = Post.query.get_or_404(post_id)
    author_settings = json.loads(post.user.settings_json)
    if author_settings["has_avatar"]:
        author_avatar = url_for('static', filename='uploads/' +
                                str(post.user.id) + '/avatar.jpg')
    else:
        author_avatar = url_for('static', filename='img/avatar.png')
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

        db.session.add(comment)
        db.session.commit()
        flash('Comment successful!')
        return redirect(url_for('post', post_id=post_id))
    return render_template('post.html', post=post, comments=packed_comments, form=form, author_avatar=author_avatar)


# Deletes post (and all respective comments via database cascade relationship)
@app.route("/delete_post/<int:post_id>")
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author_id != current_user.id:
        flash("You cannot delete this post!")
        return redirect(url_for('post', post_id=post_id))
    img = post.image_file
    if img != 'default.jpg':  # If the post has an image, delete it
        upload_dir = app.config["DEFAULT_UPLOAD_DEST"]
        user_dir = os.path.join(upload_dir, str(current_user.id))
        os.remove(os.path.join(user_dir, img))
    db.session.delete(post)
    db.session.commit()
    flash("Post deleted!")
    return redirect(url_for('home'))


# A page for the user to create a new post
@app.route("/create", methods=['GET', 'POST'])
@login_required
def create():
    session['current_page'] = url_for('create')
    settings_loader(current_user.settings_json)
    form = PostForm()
    if form.validate_on_submit():
        if form.picture.data is not None:
            if not allowed_file(form.picture.data.filename):
                flash("File type not allowed")
        post = Post(title=form.title.data, content=form.content.data,
                    author_id=current_user.id)
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
