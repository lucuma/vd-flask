# coding=utf-8
from flask import render_template

from .bp import bp


@bp.route('/')
def index():

    return render_template(
        u'public/index.html',
    )
