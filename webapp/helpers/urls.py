# coding=utf-8
from flask import request, url_for


def get_current_url(external=None, **kwargs):
    rule = request.url_rule
    if not rule:
        return '?' + '&'.join(
            ['='.join([str(k), str(v)]) for k, v in kwargs.items()]
        )
    rkwargs = request.view_args

    for key in request.values:
        values = request.values.getlist(key)
        if key in rkwargs and not isinstance(rkwargs[key], list):
            values.append(rkwargs[key])
            rkwargs[key] = values
        else:
            if len(values) == 1:
                rkwargs[key] = values[0]
            else:
                rkwargs[key] = values

    rkwargs.update(kwargs)
    for key, value in rkwargs.items():
        if not value:
            del rkwargs[key]

    rkwargs['_external'] = external
    return url_for(rule.endpoint, **rkwargs)
