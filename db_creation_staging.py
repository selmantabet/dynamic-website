# Initilaize the Flask app
from blog import app, db

# Initialize models
from blog.models import User, Post, Comment
import time
with app.app_context():
    input("Press Enter to create the database..")
    db.create_all()
    admin = User(username="admin",
                 password="pbkdf2:sha256:260000$fvjfIePE7JZj9dnG$9c838fa3ec9641177b4e5046fa941786d57c5fa576f9e2f61d5e7bd81964b2c9")
    user = User(username="user", password="pbkdf2:sha256:260000$fvjfIePE7JZj9dnG$9c838fa3ec9641177b4e5046fa941786d57c5fa576f9e2f61d5e7bd81964b2c9")
    post1 = Post(title="First Post",
                 content="This is my first post", author_id=1)
    post2 = Post(title="Second Post",
                 content="This is my second post", author_id=1)
    comment1 = Comment(content="This is my first comment",
                       post_id=1, author_id=1)
    comment2 = Comment(content="This is my first user comment",
                       post_id=1, author_id=2)
    comment3 = Comment(content="This is my second comment",
                       post_id=1, author_id=1)
    comment4 = Comment(content="This is my third comment",
                       post_id=2, author_id=1)
    comment5 = Comment(content="This is my second user comment",
                       post_id=2, author_id=2)

    items = [admin, user, post1, post2, comment1,
             comment2, comment3, comment4, comment5]
    for i in items:
        db.session.add(i)
        time.sleep(0.2)
    db.session.commit()


print("Database created.")
