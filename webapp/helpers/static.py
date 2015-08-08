# coding=utf-8
from flask import request

from .. import config


def static_url(path, external=False):
    if not path:
        return u''
    url = '/'.join([
        config.STATIC_URL,
        path.lstrip('/')
    ])
    if external:
        if url.startswith('//'):
            url = '{}:{}'.format(request.scheme, url)
        else:
            url = request.host_url.rstrip('/') + url
    return url


def upload_url(path, external=False):
    if not path:
        return u''
    url = '/'.join([
        config.UPLOADS_URL,
        path.lstrip('/')
    ])
    if external:
        if url.startswith('//'):
            url = '{}:{}'.format(request.scheme, url)
        else:
            url = request.host_url.rstrip('/') + url
    return url
