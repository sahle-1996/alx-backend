#!/usr/bin/env python3
"""A Simple Flask application with internationalization and time zone support.
"""
import pytz
from typing import Union, Dict
from flask_babel import Babel, format_datetime
from flask import Flask, render_template, request, g


class Config:
    """Configuration for Flask Babel internationalization and timezone.
    """
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


# Create the Flask application
app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False
babel = Babel(app)

users = {
    1: {'name': 'Balou', 'locale': 'fr', 'timezone': 'Europe/Paris'},
    2: {'name': 'Beyonce', 'locale': 'en', 'timezone': 'US/Central'},
    3: {'name': 'Spock', 'locale': 'kg', 'timezone': 'Vulcan'},
    4: {'name': 'Teletubby', 'locale': None, 'timezone': 'Europe/London'},
}


def retrieve_user() -> Union[Dict, None]:
    """Fetches a user based on the login ID parameter.
    """
    user_id = request.args.get('login_as', '')
    if user_id:
        return users.get(int(user_id), None)
    return None


@app.before_request
def setup_user() -> None:
    """Prepares the user object before handling the request.
    """
    user = retrieve_user()
    g.user = user


@babel.localeselector
def select_locale() -> str:
    """Selects the appropriate locale for the page.
    """
    query_str = request.query_string.decode('utf-8').split('&')
    query_dict = dict(map(
        lambda item: (item if '=' in item else f'{item}=').split('='),
        query_str,
    ))
    locale = query_dict.get('locale', '')
    if locale in app.config['LANGUAGES']:
        return locale
    user = getattr(g, 'user', None)
    if user and user['locale'] in app.config['LANGUAGES']:
        return user['locale']
    header_locale = request.headers.get('locale', '')
    if header_locale in app.config['LANGUAGES']:
        return header_locale
    return app.config['BABEL_DEFAULT_LOCALE']


@babel.timezoneselector
def select_timezone() -> str:
    """Selects the appropriate timezone for the page.
    """
    timezone = request.args.get('timezone', '').strip()
    if not timezone and g.user:
        timezone = g.user['timezone']
    try:
        return pytz.timezone(timezone).zone
    except pytz.exceptions.UnknownTimeZoneError:
        return app.config['BABEL_DEFAULT_TIMEZONE']


@app.route('/')
def index() -> str:
    """Renders the home page.
    """
    g.current_time = format_datetime()
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
