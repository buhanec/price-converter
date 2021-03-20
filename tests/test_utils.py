"""Util tests."""

import pytest

from priceconverter import util


@pytest.mark.parametrize('price, currency, amount', [
    ('$1000', 'USD', 1000.0),
    ('1000 USD', 'USD', 1000.0),
    ('$.5', 'USD', 0.5),

    ('€1000', 'EUR', 1000.0),
    ('1000€', 'EUR', 1000.0),
    ('1000 EUR', 'EUR', 1000.0),
    ('€.5', 'EUR', 0.5),
    ('.5€', 'EUR', 0.5),

    ('GBP', 'GBP', 1.0),
    ('£', 'GBP', 1.0),
])
def test_parse_price(price, currency, amount):
    assert util.parse_price(price) == (currency, amount)
