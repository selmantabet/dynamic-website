# Initilaize the Flask app
from blog import app, db

# Initialize models
import blog.models
with app.app_context():
    input("Press Enter to create the database..")
    db.create_all()
print("Database created.")
