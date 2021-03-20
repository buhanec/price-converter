"""APIs to get rates."""

from abc import ABC, abstractmethod
import datetime
from typing import Optional

import requests

__all__ = ('Rates', 'RatesApi', 'ExchangeRatesApi', 'UnsupportedCurrency')

from priceconverter import config

_START_OF_TIME = datetime.datetime.min.replace(tzinfo=datetime.timezone.utc)


def _now() -> datetime.datetime:
    return datetime.datetime.now(tz=datetime.timezone.utc)


class UnsupportedCurrency(ValueError):
    """Unsupported currency."""


class Rates(ABC):
    """Base rates API class."""

    def __init__(self,
                 cache_time: Optional[datetime.timedelta] = None,
                 cache_location: Optional[str] = None,
                 base: Optional[str] = None,
                 session: Optional[requests.Session] = None) -> None:
        if cache_time is not None:
            self.cache_time = cache_time
        else:
            self.cache_time = config.CACHE_AGE
        if cache_location is not None:
            self.cache_location = cache_location
        else:
            self.cache_location = config.CACHE_LOCATION
        if base is not None:
            self.base = base
        else:
            self.base = config.BASE
        if session is not None:
            self.session = session
        else:
            self.session = requests.Session()

    @abstractmethod
    def _get(self, ccy_1: str, ccy_2: str) -> float:
        return NotImplemented

    def get(self, ccy_1: str, ccy_2: Optional[str] = None) -> float:
        """
        Get current rate between ccy_1 and ccy_2 or ccy_1 and base.

        :param ccy_1: First currency
        :param ccy_2: Second currecny, or base currency if not specified
        :return: Curernt rate
        """
        if ccy_2 is None:
            ccy_2 = self.base
        return self._get(ccy_1, ccy_2)

    def __repr__(self) -> str:
        return (f'{type(self).__name__}('
                f'cache_time={self.cache_time!r}, '
                f'base={self.base!r})')


class RatesApi(Rates):
    """API interface for ratesapi.io."""

    URL = 'https://api.ratesapi.io/api/latest'

    def __init__(self,
                 cache_time: Optional[datetime.timedelta] = None,
                 cache_location: Optional[str] = None,
                 base: Optional[str] = None,
                 session: Optional[requests.Session] = None) -> None:
        super().__init__(cache_time, cache_location, base, session)
        self._rates = {}
        self._last_query = _START_OF_TIME

    def _get(self, ccy_1: str, ccy_2: str) -> float:
        if self._last_query + self.cache_time < _now():
            r = self.session.get(self.URL, params={'base': self.base})
            r.raise_for_status()
            r_json = r.json()
            rates = r_json['rates']
            rates[r_json['base']] = 1.0
            self._rates = rates
        if ccy_1 not in self._rates:
            raise UnsupportedCurrency(ccy_1)
        if ccy_2 not in self._rates:
            raise UnsupportedCurrency(ccy_2)
        return self._rates[ccy_1] / self._rates[ccy_2]


class ExchangeRatesApi(Rates):
    """API interface for exchangeratesapi.io."""

    URL = 'https://api.exchangeratesapi.io/latest'

    def __init__(self,
                 cache_time: Optional[datetime.timedelta] = None,
                 cache_location: Optional[str] = None,
                 base: Optional[str] = None,
                 session: Optional[requests.Session] = None) -> None:
        super().__init__(cache_time, cache_location, base, session)
        self._rates = {}
        self._last_query = _START_OF_TIME

    def _get(self, ccy_1: str, ccy_2: str) -> float:
        if self._last_query + self.cache_time < _now():
            r = self.session.get(self.URL, params={'base': self.base})
            r.raise_for_status()
            self._rates = r.json()['rates']
        if ccy_1 not in self._rates:
            raise UnsupportedCurrency(ccy_1)
        if ccy_2 not in self._rates:
            raise UnsupportedCurrency(ccy_2)
        return self._rates[ccy_1] / self._rates[ccy_2]
