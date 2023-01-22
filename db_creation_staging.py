"""
Database Test Data Generation Script

Developed by Selman Tabet @ https://selman.io/
------------------------------------------------
Developed for Coursework 2 of the CMT120 course at Cardiff University

This script populates the database with test data for development purposes.
"""
# Initilaize the Flask app
from blog import app, db

# Initialize models
from blog.models import User, Post, Comment
import time
import os
import json
from dotenv import load_dotenv
import datetime

cwd = os.getcwd()
base_env_path = os.path.join(cwd, "blog", "env", "base.env")
print("base env path: ", base_env_path)
if (os.path.exists(base_env_path)):
    load_dotenv(dotenv_path=base_env_path)
    print("base env vars initialized from db_creation")
files = ["ff.txt", "harpy.txt", "zamanya.txt",
         "cia.txt", "scraper.txt", "ph03n1x.txt"]
titles = ["Shopify Integration Gateway", "Project HARPY", "Project Zamanya",
          "Cryptocurrency Investment Adviser (CIA)", "Passport Scraper", "Project PH03N1X"]
images = ["ff.jpg", "harpy.jpg", "zamanya.jpg",
          "cia.jpg", "scraper.png", "ph03n1x.jpg"]

with app.app_context():
    input("Press Enter to create the database..")
    db.create_all()
    admin = User(username="admin", password=os.environ.get("ADMIN_PASSWORD"), creation_date=datetime.datetime(2023, 1, 15, 18, 0, 0),
                 settings_json=json.dumps({"has_avatar": False, "mode": "dark"}))
    user = User(username="user", password=os.environ.get("ADMIN_PASSWORD"),
                settings_json=json.dumps({"has_avatar": False, "mode": "dark"}))
    # posts = []
    # for i in zip(files, titles, images):
    #     with open(os.path.join("post_content", i[0]), "r") as f:
    #         content = f.read()
    #         posts.append(
    #             Post(title=i[1], content=content, author_id=1, image_file=i[2]))

    # comment1 = Comment(content="This is my first comment",
    #                    post_id=1, author_id=1)
    # comment2 = Comment(content="This is my first user comment",
    #                    post_id=1, author_id=2)
    # comment3 = Comment(content="This is my second comment",
    #                    post_id=1, author_id=1)
    # comment4 = Comment(content="This is my third comment",
    #                    post_id=2, author_id=1)
    # comment5 = Comment(content="This is my second user comment",
    #                    post_id=2, author_id=2)
    users = [admin, user]
    # comments = [comment1, comment2, comment3, comment4, comment5]
    for i in users:
        db.session.add(i)
        time.sleep(0.2)
    # for j in posts:
    #     db.session.add(j)
    #     time.sleep(0.2)
    # for k in comments:
    #     db.session.add(k)
    #     time.sleep(0.2)
    db.session.commit()
print("Database created.")
