#!/usr/bin/env python
# encoding: utf-8
from flask import Flask
from sample import sample
app = Flask(__name__)
app.register_blueprint(sample)


if __name__ == "__main__":
    app.run(debug=True)