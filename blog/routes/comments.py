"""
Application Routes - Comments

Developed by Selman Tabet @ https://selman.io/
------------------------------------------------
Developed for Coursework 2 of the CMT120 course at Cardiff University
"""

from flask import url_for, redirect, flash
from blog import app
from flask_login import current_user, login_required
from blog.utils.settings import *
from blog.models import Comment
from blog import db

# Deletes comment


@app.route("/delete_comment/<int:comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    post_id = comment.post.id
    if comment.author_id != current_user.id:
        flash("You cannot delete this comment!")
        return redirect(url_for('post', post_id=post_id))
    db.session.delete(comment)
    db.session.commit()
    flash("Comment deleted!")
    return redirect(url_for('post', post_id=post_id))
