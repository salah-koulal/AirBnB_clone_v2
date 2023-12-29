#!/usr/bin/python3
"""doc flask"""
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello():
    """start flask"""
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """start flask"""
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def printC(text):
    """Display CText"""
    return "C {}".format(text.replace("_", " "))


@app.route('/python/', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def PrintPy(text):
    """Display Python slag"""
    modified_text = text.replace("_", " ")
    return "Python {}".format(modified_text)


@app.route("/number/<int:n>", strict_slashes=False)
def OnlyNum(n):
    return "{} is a number".format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    """display slag number template"""
    return render_template('5-number.html', number=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def number_odd_or_even(n):
    """ def doc """
    if n % 2 == 0:
        p = 'even'
    else:
        p = 'odd'
    return render_template('6-number_odd_or_even.html', number=n, parity=p)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
