# coding=utf-8
from werkzeug.contrib.cache import SimpleCache, MemcachedCache

from .. import config


def get_default_cache():
    if config.MEMCHACHED_SERVERS:
        return MemcachedCache(
            servers=config.MEMCHACHED_SERVERS,
            default_timeout=0,  # 0 = no expirar nunca
            key_prefix=config.MEMCHACHED_KEY_PREFIX,
        )
    return SimpleCache()


cache = get_default_cache()
