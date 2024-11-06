#!/usr/bin/env python3
'''Task 7: Infer appropriate time zone
'''

from typing import Dict, Union
from flask import Flask, render_template, request, g
from flask_babel import Babel
import pytz


class Config:
    '''Configuration class for the application'''

    DEBUG = True
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


# Initialize the Flask application
app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False
babel = Babel(app)

user_db = {
    1: {'name': 'Balou', 'locale': 'fr', 'timezone': 'Europe/Paris'},
    2: {'name': 'Beyonce', 'locale': 'en', 'timezone': 'US/Central'},
    3: {'name': 'Spock', 'locale': 'kg', 'timezone': 'Vulcan'},
    4: {'name': 'Teletubby', 'locale': None, 'timezone': 'Europe/London'},
}


def find_user() -> Union[Dict, None]:
    """Fetch user details based on the login ID."""
    user_id = request.args.get('login_as')
    if user_id:
        return user_db.get(int(user_id))
    return None


@app.before_request
def setup_user() -> None:
    """Sets the user data in the global object before request handling."""
    g.user = find_user()


@babel.localeselector
def determine_locale() -> str:
    """Determines the best locale for the page."""
    locale_param = request.args.get('locale')
    if locale_param in app.config['LANGUAGES']:
        return locale_param
    if g.user and g.user['locale'] in app.config["LANGUAGES"]:
        return g.user['locale']
    locale_header = request.headers.get('locale', '')
    if locale_header in app.config["LANGUAGES"]:
        return locale_header
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@babel.timezoneselector
def determine_timezone() -> str:
    """Determines the best timezone for the page."""
    timezone_param = request.args.get('timezone', '').strip()
    if not timezone_param and g.user:
        timezone_param = g.user['timezone']
    try:
        return pytz.timezone(timezone_param).zone
    except pytz.exceptions.UnknownTimeZoneError:
        return app.config['BABEL_DEFAULT_TIMEZONE']


@app.route('/')
def home() -> str:
    '''Home page route

    Returns:
        html: rendered home page
    '''
    return render_template('7-index.html')


if __name__ == "__main__":
    app.run()
