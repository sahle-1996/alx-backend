#!/usr/bin/env python3
'''Task 4: Enforce locale using URL parameter
'''

from flask import Flask, render_template, request
from flask_babel import Babel


class Config:
    '''Configuration class'''

    DEBUG = True
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False
babel = Babel(app)


@babel.localeselector
def get_locale() -> str:
    """Selects the appropriate locale for the web page.

    Returns:
        str: the best matching locale
    """
    locale = request.args.get('locale', default=None)
    if locale and locale in app.config['LANGUAGES']:
        return locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index() -> str:
    '''Main route

    Returns:
        html: the homepage template
    '''
    return render_template("4-index.html")

# Uncomment this line and comment the @babel.localeselector
# You will get the error:
# AttributeError: 'Babel' object has no attribute 'localeselector'
# babel.init_app(app, locale_selector=get_locale)


if __name__ == "__main__":
    app.run()
