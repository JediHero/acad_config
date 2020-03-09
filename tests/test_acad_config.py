from acad_config import *
from acad_config import __version__
from pathlib import Path
import pytest

def test_version():
    assert __version__ == '0.1.0'

def test_as_dict():
    expected = {'example': {
        'test1': {'value1': '5', 'value2': '6'},
        'test2': {'valuea': "'ABC'", 'valueb': "'123'"}
    }}
    assert as_dict(".") == expected

def test_as_records():
    expected = [
        {'type': 'example', 'section': 'test1',
            'option': 'value1', 'value': '5'},
        {'type': 'example', 'section': 'test1',
            'option': 'value2', 'value': '6'},
        {'type': 'example', 'section': 'test2',
            'option': 'valuea', 'value': "'ABC'"},
        {'type': 'example', 'section': 'test2',
            'option': 'valueb', 'value': "'123'"}
    ]
    assert as_records(".") == expected

def test_select():
    expected = {'value1': '5', 'value2': '6'}
    assert select(['example', 'test1'], ".") == expected
    assert select(['example', 'test1', 'value1'], ".") == "5"