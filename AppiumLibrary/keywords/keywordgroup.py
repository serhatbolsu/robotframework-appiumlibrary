# -*- coding: utf-8 -*-

import sys
import inspect

from decorator import decorator

def android_only(func):
    """Decorator to mark a method as Android only."""
    def wrapper(self, *args, **kwargs):
        if not self._is_android():
            raise RuntimeError("This keyword is only available for Android devices.")
        return func(*args, **kwargs)
    return wrapper

def ios_only(func):
    """Decorator to mark a method as iOS only."""
    def wrapper(self, *args, **kwargs):
        if not self._is_ios():
            raise RuntimeError("This keyword is only available for iOS devices.")
        return func(*args, **kwargs)
    return wrapper

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
        if decorator:
            for name, method in dict.items():
                if not name.startswith('_') and inspect.isroutine(method):
                    dict[name] = decorator(_run_on_failure_decorator, method)
        return type.__new__(cls, clsname, bases, dict)


class KeywordGroup(with_metaclass(KeywordGroupMetaClass, object)):
    pass
