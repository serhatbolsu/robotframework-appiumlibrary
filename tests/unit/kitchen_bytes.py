import pytest
from kitchen.text.converters import to_bytes

def test_matching_results():
    test_str = "HelloWorld"
    bkitchen = to_bytes(test_str)
    bbytes = bytes(test_str, encoding='utf-8')
    assert bkitchen == bbytes

def test_unicode_string():
    ustring = u'A unicode \u018e string \xf1'
    bkitchen = to_bytes(ustring)
    bbytes = bytes(ustring, encoding='utf-8')
    assert bkitchen == bbytes

def test_dict():
    d = {'who': 'Ed', 'what': 'write a test'}
    dkitchen = to_bytes(d)
    dbytes = bytes(str(d), encoding='utf-8')
    assert dkitchen == dbytes