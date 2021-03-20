"""Misc utility for parsing and validation."""

import datetime
from typing import List, Tuple, Type, TYPE_CHECKING

if TYPE_CHECKING:
    from priceconverter.apis import Rates


def parse_price(string: str) -> Tuple[str, float]:
    """
    Parse price string to currency, amount pair.

    :param string: Price string
    :return: Currency, amount pair
    :raises ValueError: on invalid string
    """
    amount = ''
    currency = ''
    amount_first = None

    # Determine if currency first or amount first
    if string[0].isdigit() or string[0] in '., ':
        amount_first = True

    for char in string:
        if char.isdigit() or char in '., ':
            if amount_first and currency:
                raise ValueError(f'Invalid string: {string!r}')
            amount += char

        else:
            if not amount_first and amount:
                raise ValueError(f'Invalid string: {string!r}')
            currency += char

    if not amount:
        amount = '1.0'

    return parse_currency(currency), float(amount)


def parse_currency(string: str) -> str:
    """
    Parse currency string.

    :param string: Currency string
    :return: Normalised currency string
    :raises ValueError: on invalid string
    """
    lookup = {'$': 'USD',
              '£': 'GBP',
              '€': 'EUR'}
    if string in lookup:
        return lookup[string]
    if not len(string) == 3:
        raise ValueError(f'Invalid string: {string!r}')
    return string


def parse_timedelta(string: str) -> datetime.timedelta:
    """
    Parse timedelta from string.

    :param string: String containing timedelta description
    :return: timedelta
    :raises ValueError: on invalid string
    """
    kwargs = {'d': 'days',
              'day': 'days',
              'days': 'days',
              'h': 'hours',
              'hour': 'hours',
              'hours': 'hours',
              'm': 'minutes',
              'min': 'minutes',
              'minute': 'minutes',
              'minutes': 'minutes',
              's': 'seconds',
              'sec': 'seconds',
              'second': 'seconds',
              'seconds': 'seconds'}
    parsed = {}
    number = ''
    kwarg = ''
    for char in string:
        if char.isspace():
            continue
        if char.isdigit() or char == '.':
            if kwarg:
                parsed[kwarg] = number
                number = ''
                kwarg = ''
            number += char
        else:
            kwarg += char
    parsed[kwarg] = number

    unknown_kwargs = tuple(k for k in parsed if k not in kwargs)
    if unknown_kwargs:
        raise ValueError('Unknown kwargs: ' + ', '.join(unknown_kwargs))

    return datetime.timedelta(**{kwargs[k]: float(v)
                                 for k, v in parsed.items()})


def parse_rates_sources(string: str) -> List[Type['Rates']]:
    """
    Parse rates sources from string list.

    :param string: Rates sources string list
    :return: Rates sources
    :raises ValueError: on invalid string
    """
    # pylint: disable=import-outside-toplevel
    from priceconverter import apis

    sources = []
    for source in string.split(','):
        source = getattr(apis, source.strip(), type(None))
        if issubclass(source, apis.Rates):
            sources.append(source)
        else:
            raise ValueError(f'Unknown source: {source!r}')
    return sources
