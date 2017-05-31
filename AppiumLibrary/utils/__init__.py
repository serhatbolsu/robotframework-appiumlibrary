import six

from .applicationcache import ApplicationCache

if six.PY3:
    unicode = str

def escape_xpath_value(value):
    value = unicode(value)
    if '"' in value and '\'' in value:
        parts_wo_apos = value.split('\'')
        return "concat('%s')" % "', \"'\", '".join(parts_wo_apos)
    if '\'' in value:
        return "\"%s\"" % value
    return "'%s'" % value
