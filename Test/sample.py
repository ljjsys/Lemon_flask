#!/usr/bin/env python
# encoding: utf-8
from flask import Blueprint
sample = Blueprint('sample',__name__)


@sample.route('/')
@sample.route('/hello')
def index():
    return "This page is a blueprint page"

@sample.route('/go')
def go():
    return  "go"

@sample.route('/dash')
def dash():
    return  "dash"