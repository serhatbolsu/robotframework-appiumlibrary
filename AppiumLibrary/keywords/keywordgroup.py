import inspect

from decorator import decorator


def _run_on_failure_decorator(method, *args, **kwargs):
    try:
        return method(*args, **kwargs)
    except Exception as err:
        self = args[0]
        if hasattr(self, '_run_on_failure'):
            self._run_on_failure()
        raise err


class KeywordGroupMetaClass(type):
    def __new__(cls, clsname, bases, dict):
        for name, method in dict.items():
            if not name.startswith('_') and inspect.isroutine(method):
                dict[name] = decorator(_run_on_failure_decorator, method)
        return type.__new__(cls, clsname, bases, dict)


class KeywordGroup(object, metaclass=KeywordGroupMetaClass):
    pass
