#!/usr/bin/env python3
"""
A Simple Flask web application
"""
from typing import (
    Dict, Union
)

from flask import Flask
from flask import g, request
from flask import render_template
from flask_babel import Babel


class Config:
    """
    Configuration class for the app
    """
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


# Set up Flask application
app = Flask(__name__)
app.config.from_object(Config)

# Integrate Babel with the Flask app
babel = Babel(app)


@babel.localeselector
def determine_locale() -> str:
    """
    Determines the locale based on request parameters
    """
    locale = request.args.get('locale', '').strip()
    if locale in Config.LANGUAGES:
        return locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


users_db = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def find_user(user_id) -> Union[Dict[str, Union[str, None]], None]:
    """
    Checks if a user exists by id
    Args:
        user_id (str): The user identifier
    Returns:
        (Dict): The user information if found, otherwise None
    """
    return users_db.get(int(user_id), None)


@app.before_request
def setup_user():
    """
    Sets up the user object in the global context `g`
    """
    g.user = find_user(request.args.get('login_as', 0))


@app.route('/', strict_slashes=False)
def home() -> str:
    """
    Renders the home page HTML template
    """
    return render_template('5-index.html')


if __name__ == '__main__':
    app.run()
