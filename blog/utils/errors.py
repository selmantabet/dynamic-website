"""
Error handlers for the application.

Developed by Selman Tabet @ https://selman.io/
------------------------------------------------
Developed for Coursework 2 of the CMT120 course at Cardiff University

Contains additional routing to error pages.
"""

from blog import app
from flask import render_template


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")


@app.errorhandler(403)
def not_found(e):
    return render_template("403.html")
