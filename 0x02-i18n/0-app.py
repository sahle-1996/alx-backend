#!/usr/bin/env python3
'''Basic Flask app with a single route.'''

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    '''Default route for the home page.'''
    return render_template("0-index.html")


if __name__ == "__main__":
    app.run(debug=True)
