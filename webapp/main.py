# coding=utf-8
import logging.config

from flask import g, request
try:
    import flask_debugtoolbar
except ImportError:
    pass

from . import (
    config,
    errors,
    auth,
    public,
)
from .app import app


@app.before_request
def set_user_locale(*args, **kwargs):
    if hasattr(g, 'user') and g.user:
        request.locale = g.user.locale or config.DEFAULT_LOCALE
        request.tzinfo = g.user.tzinfo or config.DEFAULT_TIMEZONE
    else:
        request.locale = config.DEFAULT_LOCALE
        request.tzinfo = config.DEFAULT_TIMEZONE
    g.lang = request.locale.split('-')[0].lower()


app.register_blueprint(public.views.bp.bp, url_prefix='')


app.add_url_rule('/', 'index', build_only=True, redirect_to='/')

logging.config.dictConfig(config.LOGGING_CONFIG)
toolbar = flask_debugtoolbar.DebugToolbarExtension(app)


if __name__ == "__main__":
    app.run()
