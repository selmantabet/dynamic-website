# Initilaize the Flask app
from blog import app

# Initialize the routes, models and forms
import blog.models
import blog.forms
import blog.routes
print("WSGI Running..")
if __name__ == '__main__':
    print("Running Flask app from WSGI")
    app.run(debug=True)
