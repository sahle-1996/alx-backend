#!/usr/bin/env python3
'''Flask app with basic Babel configuration.'''

from flask import Flask, render_template
from flask_babel import Babel


class AppConfig:
    '''Application configuration for language and timezone.'''

    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(AppConfig)
app.url_map.strict_slashes = False

babel = Babel(app)


@app.route('/')
def home():
    '''Root route for rendering the main page.'''
    return render_template("1-index.html")


if __name__ == "__main__":
    app.run(debug=True)
