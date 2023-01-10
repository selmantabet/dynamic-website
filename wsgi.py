# Initilaize the Flask app
from blog import app as application

# Initialize the routes, models and forms
import blog.models
import blog.forms
import blog.routes
print("WSGI Running..")
if __name__ == '__main__':
    print("Running Flask app from WSGI")
    application.run(debug=True)
