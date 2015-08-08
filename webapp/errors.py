# coding=utf-8
from flask import render_template

from . import config
from .app import app
from .database import db
from .exceptions import Forbidden, NotFound, Gone, InternalServerError


@app.route('/error/forbidden/')
def forbidden(error=None):
    return render_template('public/forbidden.html'), Forbidden.code


@app.route('/error/not-found/')
def not_found(error=None):
    return render_template('public/not-found.html'), NotFound.code


def debug_not_found(error=None):
    return render_template(
        'debug-not-found.html',
        routes=app.url_map._rules
    ), NotFound.code


@app.route('/error/gone/')
def gone(error=None):
    return render_template('public/not-found.html'), Gone.code


@app.route('/error/server-error/')
def server_error(error=None):
    if error:
        db.rollback()
    return render_template('public/server-error.html'), InternalServerError.code


if not config.DEBUG:
    app.errorhandler(403)(forbidden)
    app.errorhandler(404)(not_found)
    app.errorhandler(410)(gone)
    app.errorhandler(500)(server_error)
else:
    app.errorhandler(404)(debug_not_found)
