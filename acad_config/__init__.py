"""Returns the configuration values stored in a file as a nested dict or record
and provides utiltiy functions for accessing those values.

By default, config files are saved as file_name.ini files in the ~/.config/acad_config
directory.

example file saved at ~/.config/acad_config/example.ini
[test1]
value1 = 5
value2 = 6

[test2]
valuea = 'ABC'
valueb = '123'

>>> as_dict()
{'example': {
    'test1': {'value1': '5', 'value2': '6'},
    'test2': {'valuea': "'ABC'", 'valueb': "'123'"}
}}
>>> as_records()
[
    {'type': 'example', 'section': 'test1',
        'option': 'value1', 'value': '5'},
    {'type': 'example', 'section': 'test1',
        'option': 'value2', 'value': '6'},
    {'type': 'example', 'section': 'test2',
        'option': 'valuea', 'value': "'ABC'"},
    {'type': 'example', 'section': 'test2',
        'option': 'valueb', 'value': "'123'"}
]
>>> select(['example', 'test1'])
{'value1': '5', 'value2': '6'}
>>> select(['example', 'test1', 'value1'])
5

If example.ini were saved in the working directory then
>>> as_dict('.')
{'example': {
    'test1': {'value1': '5', 'value2': '6'},
    'test2': {'valuea': "'ABC'", 'valueb': "'123'"}
}}
"""
__version__ = '0.1.0'
from configparser import ConfigParser
from pathlib import Path
import typing as tp

import toolz as tz

FilePath = tp.Union[Path, str]
Record = tp.Dict[str,tp.Any]

def as_dict(location: tp.Optional[FilePath]=None) -> tp.Dict[str, tp.Dict]:
    """Returns configurations as a nested dict. Keys and values are strings."""
    if isinstance(location, str):
        location = Path(location).expanduser()
    elif isinstance(location, Path):
        location = location.expanduser()
    else:
        location = Path("~/.config/acad_config").expanduser()

    config = ConfigParser()
    files = list(location.glob("**/*.ini"))
    result = {}
    for file in files:
        result[file.stem] = {}
        config.read(file)
        sections = config.sections()
        for section in sections:
            options = {k: v for k, v in config[section].items()}
            result[file.stem][section] = options
    return result

def as_records(location: tp.Optional[FilePath]=None) ->tp.List[Record]:
    """Returns configuratoins as a list of dicts."""
    settings = as_dict(location)
    result = []
    for file, sections in settings.items():
        for section, options in sections.items():
            for option, value in options.items():
                row = {
                    "type": file,
                    "section": section,
                    "option": option,
                    "value": value,
                }

                result.append(row)
    return result

def select(keys: tp.List[str], location: tp.Optional[FilePath]=None) -> tp.Any:
    """Returns the configuration a nested dict or value."""
    settings = as_dict(location)
    return tz.get_in(keys, settings)