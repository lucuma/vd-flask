# coding=utf-8
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict


class DictSerializable(object):
    """Makes an object serializable to a dictionary.
    """

    def _asdict(self):
        result = OrderedDict()
        for key in self.__mapper__.c.keys():
            result[key] = getattr(self, key)
        return result
