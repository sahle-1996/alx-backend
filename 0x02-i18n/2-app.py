#!/usr/bin/env python3
'''Flask app for language selection from request.
'''

from flask import Flask, render_template, request
from flask_babel import Babel


class AppConfiguration:
    '''Application configuration for Babel.'''

    DEBUG = True
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(AppConfiguration)
app.url_map.strict_slashes = False
babel = Babel(app)


@babel.localeselector
def select_locale() -> str:
    """Determines the best match locale.

    Returns:
        str: matched locale
    """
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def homepage() -> str:
    '''Route for the homepage.

    Returns:
        html: rendered template for homepage
    '''
    return render_template("2-index.html")


if __name__ == "__main__":
    app.run()
