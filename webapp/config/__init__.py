# coding=utf-8
import io
import os
from os.path import join, dirname


DEFAULT_ENV = 'development'
APP_ENV = 'APP_ENV'
ENV_FILE = join(dirname(__file__), '..', '..', '.APP_ENV')


def get_env(default=DEFAULT_ENV):
    env = os.getenv(APP_ENV)
    if env:
        return env.strip()
    try:
        with io.open(ENV_FILE, 'rt') as f:
            env = f.read()
            os.environ[APP_ENV] = env
            return env.strip()
    except IOError:
        return default


def env_is(env):
    curr_env = get_env()
    return curr_env == env


if env_is('production'):
    from .production import *
else:
    from .development import *

# Import local settings
try:
    from .local import *
except ImportError:
    pass

if env_is('pytest'):
    from .pytest import *
