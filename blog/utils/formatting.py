"""
Formatting functions

Developed by Selman Tabet @ https://selman.io/
------------------------------------------------
Developed for Coursework 2 of the CMT120 course at Cardiff University

Contains template filters for use within Jinja2 templates.
"""

from blog import app
import babel


@app.template_filter('time_print')
def format_datetime(value, format='full_date'):
    if format == 'full_date':
        format = "EEEE, d MMMM y 'at' HH:mm"
    elif format == 'comment_date':
        format = "dd.MM.y HH:mm"
    elif format == 'join_date':
        format = "dd.MM.y"
    return babel.dates.format_datetime(value, format)
