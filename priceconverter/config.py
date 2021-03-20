"""Price converter config."""

import configparser
import datetime
import os.path
import sys
from types import MappingProxyType
from typing import Any, Sequence

from priceconverter import util

__all__ = ('BASE', 'RATES_SOURCES', 'CACHE_AGE', 'CACHE_LOCATION')

config = configparser.ConfigParser()

BASE: str
RATES_SOURCES: Sequence[str]
CACHE_AGE: datetime.timedelta
CACHE_LOCATION: str

_NAME = 'priceconverter'
_CONF_NAME = 'priceconverter.ini'
if sys.platform == 'win32':
    _LOCAL = os.path.join(os.path.expandvars('%localappdata%'), _NAME)
    _EXTRA_CONF = tuple()
else:
    _LOCAL = os.path.join(os.path.expanduser('~'), _NAME)
    _EXTRA_CONF = os.path.join('etc', _CONF_NAME)

_SEARCH_PATHS = (_CONF_NAME,
                 f'.{_CONF_NAME}',
                 os.path.join(_LOCAL, _CONF_NAME),
                 *_EXTRA_CONF)

config.read(_SEARCH_PATHS)

_CONFIGS = MappingProxyType({
    'BASE': ('USD', util.parse_currency),
    'RATES_SOURCES': ('RatesApi,ExchangeRatesApi', util.parse_rates_sources),
    'CACHE_AGE': ('1 hour', util.parse_timedelta),
    'CACHE_LOCATION': (_LOCAL, lambda x: x),
})


class ConfigurationError(RuntimeError):
    """Configuration error."""

    def __init__(self, key: str, value: str) -> None:
        super().__init__(f'Bad {key!r}: {value!r}')


def __getattr__(name: str) -> Any:
    if name not in _CONFIGS:
        raise AttributeError(name)
    fallback, parser = _CONFIGS[name]
    key = ''.join(s.capitalize() for s in name.split('_'))
    value = config.get('DEFAULT', key, fallback=fallback)
    try:
        return parser(value)
    except ValueError as e:
        raise ConfigurationError(key, value) from e
