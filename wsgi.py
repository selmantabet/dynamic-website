"""
Main WSGI Application

Developed by Selman Tabet @ https://selman.io/
------------------------------------------------
Developed for Coursework 2 of the CMT120 course at Cardiff University

This is where the application is served.
"""

# Initilaize the Flask app
from blog import app as application

# Initialize the routes, models and forms
import blog.models
import blog.forms
import blog.router
print("WSGI Running..")
if __name__ == '__main__':
    print("Running Flask app from WSGI")
    application.run(debug=True)
