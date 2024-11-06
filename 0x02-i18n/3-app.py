#!/usr/bin/env python3
'''Task 2: Fetch locale based on request.
'''

from flask import Flask, render_template, request
from flask_babel import Babel


class AppConfig:
    '''Application configuration for localization.'''

    DEBUG = True
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(AppConfig)
app.url_map.strict_slashes = False
babel = Babel(app)


@babel.localeselector
def choose_locale() -> str:
    """Selects the best matching locale for the request.

    Returns:
        str: the best matching locale.
    """
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def home() -> str:
    '''Home route.

    Returns:
        html: renders the homepage template
    '''
    return render_template("3-index.html")


if __name__ == "__main__":
    app.run()
