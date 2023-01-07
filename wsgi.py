from blog import app
import blog.models
import blog.forms
import blog.routes
print("WSGI Running..")
if __name__ == '__main__':
    print("Running Flask app from WSGI")
    app.run(debug=True)
