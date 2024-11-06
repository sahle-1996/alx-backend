#!/usr/bin/env python3
"""
A Simple Flask web application
"""
from typing import Dict, Union
from flask import Flask, g, request, render_template
from flask_babel import Babel


class Config:
    """
    Configuration class for application settings
    """
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


# Initialize the Flask app instance
app = Flask(__name__)
app.config.from_object(Config)

# Integrating Babel with the application
babel = Babel(app)


users_db = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def fetch_user(id: int) -> Union[Dict[str, Union[str, None]], None]:
    """
    Checks if a user exists based on their ID.
    Args:
        id (int): User ID
    Returns:
        dict: A user dictionary or None if user not found
    """
    return users_db.get(id)


@babel.localeselector
def get_locale() -> str:
    """
    Determine and select the locale for the application
    """
    preferred_locale = request.args.get('locale', '').strip()
    user_locale = g.user.get('locale') if g.user else None
    available_locales = [
        preferred_locale,
        user_locale,
        request.accept_languages.best_match(app.config['LANGUAGES']),
        Config.BABEL_DEFAULT_LOCALE
    ]
    for locale in available_locales:
        if locale and locale in Config.LANGUAGES:
            return locale


@app.before_request
def set_user() -> None:
    """
    Before each request, associate the user with the global `g` object
    """
    user_id = request.args.get('login_as', 0)
    g.user = fetch_user(int(user_id))


@app.route('/', strict_slashes=False)
def home() -> str:
    """
    Renders the main page of the application
    """
    return render_template('6-index.html')


if __name__ == '__main__':
    app.run()
