from blog import app, db

# Initialize models
from blog.models import Post, Comment
import time
with app.app_context():
    input("Press Enter to populate test user content..")
    post1 = Post(title="First Post",
                 content="This is my first test post", author_id=3)
    post2 = Post(title="Second Post",
                 content="This is my second test post", author_id=3)

    comment1 = Comment(content="This is my first test comment",
                       post_id=1, author_id=3)

    comment2 = Comment(content="This is my second test comment",
                       post_id=2, author_id=3)

    items = [post1, post2,
             comment1, comment2]
    for i in items:
        db.session.add(i)
        time.sleep(0.2)
    db.session.commit()


print("Test cases created.")
