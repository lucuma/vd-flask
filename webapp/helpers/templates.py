# coding=utf-8
from fnmatch import fnmatch
from os.path import dirname
import re
from xml.sax.saxutils import quoteattr

from flask import request, url_for
from markupsafe import Markup


def dumb_pluralize(num, singular=u'', plural='s'):
    return singular if num == 1 else plural


def html_attrs(classes=None, **kwargs):
    """Generate HTML attributes from the provided keyword arguments.

    The output value is sorted by the passed keys, to provide a consistent
    output.  Because of the frequent use of the normally reserved keyword
    `class`, `classes` is used instead. Also, all underscores are translated
    to regular dashes.

    Set any property with a `True` value.

    >>> html_attrs({'id': 'text1', 'classes': 'myclass', 'data_id': 1, 'checked': True})
    u'class="myclass" data-id="1" id="text1" checked'

    """
    attrs = []
    props = []

    classes = classes.strip()
    if classes:
        classes = quoteattr(classes)
        attrs.append('class=%s' % classes)

    for key, value in kwargs.iteritems():
        key = key.replace('_', '-')
        if isinstance(value, bool):
            if value is True:
                props.append(key)
        else:
            value = quoteattr(value)
            attrs.append(u'%s=%s' % (key, value))

    attrs.sort()
    props.sort()
    attrs.extend(props)
    return u' '.join(attrs)


URL_RE = re.compile((r'^([a-z]{3,7}:(//)?)?([^/:]+%s|([0-9]{1,3}\.){3}'
                    '[0-9]{1,3})(:[0-9]+)?(\/.*)?$'), re.IGNORECASE)


def _norm_url(url, path=None):
    path = path or request.path
    url = url.rstrip('/')
    if url.startswith('/'):
        return url
    baseurl = dirname(path.strip('/'))
    if baseurl:
        return '/' + '/'.join([baseurl, url])
    return '/' + url


def active(endpoint, partial=False, path=None):
    path = path or request.path
    path = path.rstrip('/')

    patterns = endpoint if isinstance(endpoint, (list, tuple)) else [endpoint]
    patterns = [p if p.startswith('/') or re.match(URL_RE, p) else url_for(p)
                for p in patterns]

    for url in patterns:
        url = _norm_url(url)
        _url = url.rstrip('/').split('#')[0]
        if fnmatch(path, _url) or (partial and path.startswith(_url)):
            return 'active'
    return u''


def link_to(text='', endpoint='', classes='', wrapper=None,
            partial=False, path=None, **kwargs):
    """Build an HTML anchor element for the provided URL.
    If the url match the beginning of that in the current request, an `active`
    class is added.  This is intended to be use to build navigation links.

    Other HTML attributes are generated from the keyword argument
    (see the `html_attrs` function).

    Example:

        >>> link_to('Hello', '/hello/', title='click me')
        u'<a href="/hello/" title="click me">Hello</a>'
        >>> link_to('Hello', '/hello/', wrapper='li', classes='last')
        u'<li class="last"><a href="/hello/">Hello</a></li>'

        >>> from werkzeug.test import EnvironBuilder
        >>> from flask import local, Request

        >>> builder = EnvironBuilder(method='GET', path='/foo/')
        >>> env = builder.get_environ()
        >>> local.request = Request(env)
        >>> link_to('Bar', '/foo/')
        u'<a href="/foo/" class="active">Bar</a>'

    :param text:
        The text (or HTML) of the link.

    :param endpoint:
        URL or endpoint name. This can also be a *list* of URLs and/or
        endpoint names. The first one will be used for the link, the rest only
        to match the current page

    :param classes:
        Because of the frequent use of the normally reserved keyword
        `class`, `classes` is used instead.

    :param wrapper:
        Optional tag name of a wrapper element for the link.
        The "active" class and other attributes will be applied to this
        element instead of the <a>. Example:

        >>> link_to('Hello', '/hello/', wrapper='li', title='Hi')
        u'<li title="Hi"><a href="/hello/">Hello</a></li>'

    :param partial:
        If True, the endpoint will be matched against the beginning of the
        current URL. For instance, if the current URL is `/foo/bar/123/`,
        an endpoint like `/foo/bar/` will be considered a match.

    :param kwargs:
        Extra HTML attributes. All underscores will be translated to
        regular dashes.

    """
    path = path or request.path
    path = path.split('#')[0].rstrip('/')

    patterns = endpoint if isinstance(endpoint, (list, tuple)) else [endpoint]
    patterns = [p if p.startswith('/') or re.match(URL_RE, p) else url_for(p)
                for p in patterns]

    for url in patterns:
        url = _norm_url(url)
        _url = url.split('#')[0].rstrip('/')
        if fnmatch(path, _url) or (partial and path.startswith(_url)):
            classes += ' active'
            break

    data = {
        'url': patterns[0],
        'text': text,
        'attrs': html_attrs(classes, **kwargs),
    }
    data['attrs'] = ' ' + data['attrs'] if data['attrs'] else ''
    if wrapper:
        data['wr'] = str(wrapper).lower()
        tmpl = u'<%(wr)s %(attrs)s><a href="%(url)s">%(text)s</a></%(wr)s>'
    else:
        tmpl = u'<a href="%(url)s"%(attrs)s>%(text)s</a>'
    return Markup(tmpl % data)


def format_file_size(num):
    for x in ['bytes', 'KB', 'MB', 'GB']:
        if num < 1024.0:
            if float(int(num)) == num:
                return "%s %s" % (int(num), x)
            return "%3.1f %s" % (num, x)
        num /= 1024.0
    return "%3.1f %s" % (num, 'TB')
