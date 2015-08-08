# coding=utf-8
import webassets

from . import config


assets_env = webassets.Environment(
    config.STATIC_PATH,
    config.STATIC_URL
)

assets_env.config['CLOSURE_COMPRESSOR_OPTIMIZATION'] = 'SIMPLE_OPTIMIZATIONS'


assets_env.register(
    'css-auth',

    'styles/auth.css',

    filters='cssmin',
    output='styles/auth.min.css'
)

assets_env.register(
    'css-main',

    'styles/main.css',

    filters='cssmin',
    output='styles/styles.min.css'
)

assets_env.register(
    'js-main',

    'scripts/jquery.min.js',
    'scripts/subforms.js',
    'scripts/main.js',

    filters='closure_js',
    output='scripts/scripts.min.js'
)
